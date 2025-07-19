import sys,os
from flask import Flask, render_template, request, redirect, request, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt     # 密码加密
import click
from flask_cors import CORS, cross_origin
from sqlalchemy import func, cast, String, desc
from flask_migrate import Migrate
from datetime import datetime,timedelta

WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)
migrate = Migrate(app, db)
VKEY="iamthemanager"
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)

app.config.from_object(__name__)

#加载用户的回调函数
@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False)
    password = db.Column(db.String(24), nullable=False)
    role = db.Column(db.Integer, nullable=False)    #0表示普通用户，1表示管理员
    analysis_id=db.Column(db.Integer)
    update_id=db.Column(db.Integer)
    address = db.Column(db.String(64))  #邮箱

    # def __init__(self, username, password,role,analysis_id,update_id):
    #     self.username = username
    #     self.password = password
    #     self.role = role
    #     self.analysis_id=analysis_id
    #     self.update_id=update_id
#采样点位置信息
class SamplePos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lon = db.Column(db.Float, nullable=False)
    lat = db.Column(db.Float, nullable=False)

#海水信息
class Ocean_Info(db.Model, UserMixin):
    info_id = db.Column(db.Integer, primary_key=True)
    loc_id = db.Column(db.Integer, nullable=False)  #采样点位置信息,外键
    time = db.Column(db.Date, nullable=False)   #采样时间
    temperature = db.Column(db.Float, nullable=False)
    sea_level = db.Column(db.Float, nullable=False)
    User_id = db.Column(db.Integer, nullable=False)  #录入信息用户

#数据维护操作信息
class Update_record(db.Model, UserMixin):
    ud_id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Date, nullable=False)   #修改时间，上面的是采样时间，不一样的
    info_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False) #操作用户id
    edit_content = db.Column(db.String(128))  #修改内容

#分析报告信息，待改
class Report(db.Model, UserMixin):
    report_id = db.Column(db.Integer, primary_key=True)
    var_tmp = db.Column(db.Float, nullable=False)
    var_level = db.Column(db.Float, nullable=False)
    pred_tmp = db.Column(db.Float, nullable=False)
    pred_level = db.Column(db.Float, nullable=False)

#执行flask initdb命令就可以创建数据库表,使用--drop选项可以删除表后重新创建
@app.cli.command()  # 注册为命令，可以传入 name 参数来自定义命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息

#路由：主页
@app.route('/')
def index():
    # return render_template('index.html')
    return 'Hello, World!'

# 登录
@app.route('/login', methods=['GET','POST'])
@cross_origin(supports_credentials=True)
def login():
    data = request.form
    username = data.get('username')
    password = data.get('password')
    print(username, password)

    # 查询用户（仅根据用户名查询）
    user = User.query.filter_by(username=username).first()

    # 加密密码匹配
    if user and user.password==password:
        return jsonify({'status': 'success', 'message': 'Login successful', "user_id": user.id,"user_type":user.role}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Invalid username or password'}), 401

#路由：注册
@app.route('/register', methods=['GET', 'POST'])
# @cross_origin(supports_credentials=True)
def register():
    print("register in!!!!!")
    try:
        if request.method == 'POST':
            # 用户注册
            latest_user = User.query.order_by(User.id.desc()).first()
            id = latest_user.id + 1 if latest_user else 1
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            user_type = int(request.form['userType'])
            invite_code = None
            if user_type == 1:
                invite_code = request.form['inviteCode']
                if invite_code not in ["kjk123456", "kjk654321", "kjk666888"]:
                    print("invalid")
                    return "error: invite code invalid", 401

            # 加密密码
            # hashed_password = bcrypt.generate_password_hash(
            #     password).decode('utf-8')

            # default_avatar_url = 'http://graphcrafter.oss-cn-beijing.aliyuncs.com/avatars/1-default.webp'
            user_now = User(id=id, username=username, password=password, address=email, role=user_type)
            print(user_now)
            # 用户名已占用
            users = User.query.filter_by(username=username).all()
            if users:
                return "error: username already taken", 400
            # 用户名未占用，可注册
            db.session.add(user_now)
            db.session.commit()
            return 'success', 200
        return '', 405
    except Exception as e:
        # 捕获异常并记录错误信息
        app.logger.error(f"Error during registration: {e}")
        return "Internal Server Error", 500

#路由：获取用户名
@app.route('/get_user/<int:user_id>', methods=['GET', 'POST'])
# @cross_origin(supports_credentials=True)
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        return jsonify({'username': user.username, 'role': user.role,'add':user.address,'password':user.password}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Invalid user id'}), 404

#路由：获取信息管理界面表格内容
@app.route('/get_table', methods=['GET'])
# @cross_origin(supports_credentials=True)
def get_table():
    tables = db.session.query(
        Ocean_Info.info_id,
        SamplePos.id,
        SamplePos.lon,
        SamplePos.lat,
        cast(Ocean_Info.time, String),
        Ocean_Info.temperature,
        Ocean_Info.sea_level,
        User.username
    ).join(User,User.id==Ocean_Info.User_id) .outerjoin(SamplePos, SamplePos.id == Ocean_Info.loc_id) \
    .order_by((Ocean_Info.info_id)) \
    .all()

    tables_data=[]
    for data in tables:
        table_data={
            'id':data[0],
            'pos':data[1],
            'lon':data[2],
            'lat':data[3],
            'date':data[4][:19],
            'temp':data[5],
            'sl':data[6],
            'user_id':data[7]
        }
        tables_data.append(table_data)
    return jsonify({'dataList':tables_data}), 200

#路由：增添数据，同时加入到修改记录中
@app.route('/add_info', methods=['POST'])
@cross_origin(supports_credentials=True)
def add_info():
    print("in=============================")
    data = request.form  
    print(data)  
    pos = data.get('pos')
    lon=data.get('lon')
    lat=data.get('lat')
    print("lon======================")
    print(lon)
    #先看一下这个位置记录过没有
    element = SamplePos.query.filter_by(lon=lon,lat=lat).first()
    if element:
        pos=element.id
    else:
        new_element = SamplePos(lon=lon,lat=lat)
        db.session.add(new_element)
        db.session.commit()
        pos=new_element.id   

    date1 = data.get('date1')
    date2 = data.get('date2')
    # print(date1)   
    # print(date2)

    date = date2
    if date.endswith('Z'):
        date = date[:-1] 
    # 将字符串转换为 datetime 对象
    date_object = datetime.fromisoformat(date)

    temp = data.get('temp')
    sl = data.get('sl')
    user_id = data.get('user_id')
    
    #插入数据
    new_info = Ocean_Info(loc_id=pos, time=date_object, temperature=temp, sea_level=sl, User_id=user_id)
    db.session.add(new_info)
    db.session.commit()
    content = 'id:'+str(new_info.info_id)+';pos:'+str(pos)+';lon:'+str(lon)+';lat:'+str(lat)\
            +';temp:'+str(temp)+';date:'+str(date)+';sl:'+str(sl)+';user_id:'+str(user_id)
    new_record = Update_record(time=datetime.now(), info_id=new_info.info_id, user_id=user_id, edit_content=content)
    db.session.add(new_record)
    db.session.commit()
    return jsonify({'id': new_info.info_id,'pos':pos,'time':date_object}), 200

#路由：增添数据，同时加入到修改记录中
@app.route('/edit_save', methods=['POST','GET'])
@cross_origin(supports_credentials=True)
def edit_save():
    print("in=============================")
    data = request.get_json()
    id = data.get('id')
    print('id==========================')
    print(id)
    # pos = data.get('pos')
    lon=data.get('lon')
    lat=data.get('lat')
     #先看一下这个位置记录过没有
    element = SamplePos.query.filter_by(lon=lon,lat=lat).first()
    if element:
        pos=element.id
    else:
        new_element = SamplePos(lon=lon,lat=lat)
        db.session.add(new_element)
        db.session.commit()
        pos=new_element.id   
    
    temp = data.get('temp')
    date = data.get('date')
    if date.endswith('Z'):
        date = date[:-1] 
    # 将字符串转换为 datetime 对象
    date_object = datetime.fromisoformat(date)
    print(type(date))
    sl = data.get('sl')
    user_id = data.get('current_user')
    item=Ocean_Info.query.get(id)
    if item:
        item.loc_id=pos
        item.temperature=temp
        item.time=date_object
        item.sea_level=sl
        item.User_id=user_id
        print("item====================")
        print(item.loc_id,item.temperature,item.time,item.sea_level,item.User_id)
        db.session.commit()
        #修改历史里添加
        content = 'id:'+str(id)+';pos:'+str(pos)+';lon:'+str(lon)+';lat:'+str(lat)\
            +';temp:'+str(temp)+';date:'+str(date)+';sl:'+str(sl)+';user_id:'+str(user_id)
        new_record = Update_record(time=datetime.now(), info_id=id, user_id=user_id, edit_content=content)
        db.session.add(new_record)
        db.session.commit()
        return jsonify({'status': 'success', 'pos': pos}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Invalid id'}), 404
 
@app.route('/delete_info', methods=['POST'])
def delete_info():
    print("delete================")
    row = request.get_json()
    print(row)
    id = row.get('id')
    # 查询数据库中的项
    info = Ocean_Info.query.get(id)
    # 如果找到了项，删除它
    if info:
        db.session.delete(info)
        db.session.commit()
    return '', 204

#路由：增添数据，同时加入到修改记录中
@app.route('/draw_data_temp_pos/<int:pos>', methods=['GET'])
@cross_origin(supports_credentials=True)
def draw_data_temp_pos(pos):
    #获取Ocean_Info中的所有海洋温度+时间数据
    
    datas = db.session.query(
        Ocean_Info.time,
        Ocean_Info.temperature
    ).filter(Ocean_Info.loc_id==pos)  \
        .all()
    data=[]
    for d in datas:
        date_string = d[0].strftime("%Y-%m-%d")
        data.append({'name':date_string,'value':d[1]})
    return jsonify({'data':data}), 200

@app.route('/draw_data_temp_date/<string:date>', methods=['GET'])
@cross_origin(supports_credentials=True)
def draw_data_temp_date(date):
    #获取Ocean_Info中的所有海洋温度+时间数据
    datas = db.session.query(
        Ocean_Info.loc_id,
        Ocean_Info.temperature
    ).filter(Ocean_Info.time==date)  \
        .all()
    data=[]
    for d in datas:
        # date_string = d[0].strftime("%Y-%m-%d")
        data.append({'name':d[0],'value':d[1]})
    return jsonify({'data':data}), 200


#路由：增添数据，同时加入到修改记录中
@app.route('/draw_data_sea_level_pos/<int:pos>', methods=['GET'])
@cross_origin(supports_credentials=True)
def draw_data_sea_level_pos(pos):
    #获取Ocean_Info中的所有海洋温度+时间数据
    datas = db.session.query(
        Ocean_Info.time,
        Ocean_Info.sea_level
    ).filter(Ocean_Info.loc_id==pos).all()
    data=[]
    for d in datas:
        date_string = d[0].strftime("%Y-%m-%d")
        data.append({'name':date_string,'value':d[1]})
    return jsonify({'data':data}), 200

@app.route('/draw_data_sea_level_date/<string:date>', methods=['GET'])
@cross_origin(supports_credentials=True)
def draw_data_sea_level_date(date):
    #获取Ocean_Info中的所有海洋温度+时间数据
    datas = db.session.query(
        Ocean_Info.loc_id,
        Ocean_Info.sea_level
    ).filter(Ocean_Info.time==date).all()
    data=[]
    for d in datas:
        # date_string = d[0].strftime("%Y-%m-%d")
        data.append({'name':d[0],'value':d[1]})
    return jsonify({'data':data}), 200

@app.route('/api/get_pos_key', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_pos_key():
    keys = [row.id for row in SamplePos.query.with_entities(SamplePos.id).all()]
    return jsonify(keys)

@app.route('/api/get_date_key', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_date_key():
    keys = [row.time.strftime("%Y-%m-%d") for row in db.session.query(Ocean_Info.time).distinct()]
    return jsonify(keys)

#=======================获取编辑历史=======================================
@app.route('/get_history', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_history():
    tables = db.session.query(
        Update_record.ud_id,
        cast(Update_record.time, String),
        Update_record.info_id,
        User.username,
        Update_record.edit_content
    ).join(User, User.id == Update_record.user_id) \
    .order_by(desc(Update_record.ud_id)).all()
    tables_data=[]
    for data in tables:
        table_data={
            'id':data[0],
            'date':data[1],
            'info_id':data[2],
            'user_id':data[3],
            'content':data[4]
        }
        tables_data.append(table_data)
    return jsonify({'dataList':tables_data}), 200

@app.route('/delete_history', methods=['POST'])
def delete_history():
    print("delete================")
    row = request.get_json()
    print(row)
    id = row.get('id')
    # 查询数据库中的项
    info = Update_record.query.get(id)
    # 如果找到了项，删除它
    if info:
        db.session.delete(info)
        db.session.commit()
    return '', 204

@app.route('/edit_user', methods=['POST'])
@cross_origin(supports_credentials=True)
def edit_user():
    print("in=============================")
    data = request.get_json()
    user_id = data.get('user_id')
    print('id==========================')
    # print(id)
    # pos = data.get('pos')
    username=data.get('username')
    add=data.get('add')
    password=data.get('password')
    
    item=User.query.get(user_id)
    if item:
        item.username=username
        item.address=add
        item.password=password        
        db.session.commit()        
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Invalid id'}), 404

@app.route('/predict/<int:pos>', methods=['GET'])
@cross_origin(supports_credentials=True)
def predict(pos):
    tables = db.session.query(
        Ocean_Info.time,
        Ocean_Info.temperature,
        Ocean_Info.sea_level
    ).filter(Ocean_Info.loc_id==pos).all()

    datas_temp=[]
    for item in tables:
        date_string = item[0].strftime("%Y-%m-%d")
        datas_temp.append({'name':date_string,'value':item[1]})
    #按照时间升序排序
    datas_temp.sort(key=lambda x:x['name'])

    datas_sl=[]
    for item in tables:
        date_string = item[0].strftime("%Y-%m-%d")
        datas_sl.append({'name':date_string,'value':item[2]})
    #按照时间升序排序
    datas_sl.sort(key=lambda x:x['name'])

    #取最后两个值
    if len(datas_temp)<2:
        return jsonify({'status': 'error', 'message': 'Not enough data'}), 404
    else:
        #计算斜率
        k1 = (datas_temp[-1]['value']-datas_temp[-2]['value'])/(tables[-1][0]-tables[-2][0]).days
        k2 = (datas_sl[-1]['value']-datas_sl[-2]['value'])/(tables[-1][0]-tables[-2][0]).days

        pred_temp = round(datas_temp[-1]['value']+k1*(tables[-1][0]-tables[-2][0]).days,2)
        pred_sl = round(datas_sl[-1]['value']+k2*(tables[-1][0]-tables[-2][0]).days,2)

        #计算时间加(datas_temp[-1]['name']-datas_temp[-2]['name']).days
        new_date=tables[-1][0]+timedelta(days=(tables[-1][0]-tables[-2][0]).days)
        new_date_string =new_date.strftime("%Y-%m-%d")

        datas_temp.append({'name':new_date_string,'value':pred_temp})
        datas_sl.append({'name':new_date_string,'value':pred_sl})

        return jsonify({'new_date':new_date_string,
                        'data_temp':datas_temp,
                        'pred_temp': pred_temp,
                        'data_sl':datas_sl,
                        'pred_sl':pred_sl,}), 200
    
    #路由：获取用户名
@app.route('/get_all_user', methods=['GET', 'POST'])
# @cross_origin(supports_credentials=True)
def get_all_user():
    users = User.query.all()
    users_data=[]
    for user in users:
        user_data={
            'id':user.id,
            'username':user.username,
            'role':user.role,
            'add':user.address,
            'password':user.password
        }
        users_data.append(user_data)
    return jsonify({'dataList':users_data}), 200

@app.route('/delete_user/<int:userid>', methods=['GET', 'POST'])
# @cross_origin(supports_credentials=True)
def delete_user(userid):
    
    info = User.query.get(userid)
    # 如果找到了项，删除它
    if info:
        db.session.delete(info)
        db.session.commit()
    return '', 204

app.debug=True
app.run()
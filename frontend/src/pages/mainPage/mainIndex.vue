<template>
    <div class="container">
      <div class="top">
        <header class="mask-paper">
          <img src="../../assets/logo.png" class="logo" />
          <div class="welcome">Welcome</div>
          <div class="downbar">
            <el-dropdown>
              <span class="el-dropdown-link">
                {{ username }}
                <el-icon class="el-icon--right">
                  <arrow-down />
                </el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="handleEdit">编辑资料</el-dropdown-item>
                  <el-dropdown-item @click="Logout">退出登陆</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </header>
      </div>
      <div class="main">
        <div class="side-bar" style="z-index:10">
          <ul class="channel-list">
            <li :class="{ 'active-channel': activeChannel === 'manage' }">
              <a class="link-wrapper" @click="toManage">
                <House style="width: 1em; height: 1em; margin-right: 8px" /><span class="channel">数据管理</span>
              </a>
            </li>
            <li :class="{ 'active-channel': activeChannel === 'analysis' }">
              <a class="link-wrapper" @click="toAnalysis">
                <DataAnalysis style="width: 1em; height: 1em; margin-right: 8px" /><span class="channel">数据分析</span>
              </a>
            </li>
            <ul v-if="activeChannel === 'analysis' || activeChannel === 'charts' || activeChannel === 'map'" class="sub-menu">
              <li :class="{ 'active-channel': activeChannel === 'charts' }" @click="toCharts">
                <a class="link-wrapper">
                  <DataAnalysis style="width: 1em; height: 1em; margin-right: 8px" /><span class="channel">图表分析</span>
                </a>
              </li>
              <li :class="{ 'active-channel': activeChannel === 'map' }" @click="toMap">
                <a class="link-wrapper">
                  <MapLocation style="width: 1em; height: 1em; margin-right: 8px" /><span class="channel">地图展示</span>
                </a>
              </li>
            </ul>
            <!-- <li :class="{ 'active-channel': activeChannel === 'map' }">
              <a class="link-wrapper" @click="toMap">
                <DataAnalysis style="width: 1em; height: 1em; margin-right: 8px" /><span class="channel">地图</span>
              </a>
            </li> -->
            
            <li :class="{ 'active-channel': activeChannel === 'userManage' }">
              <a class="link-wrapper" @click="toUserManage">
                <User style="width: 1em; height: 1em; margin-right: 8px" /><span class="channel">用户管理</span>
              </a>
            </li>
            <li :class="{ 'active-channel': activeChannel === 'history' }">
              <a class="link-wrapper" @click="toHistory">
                <Calendar style="width: 1em; height: 1em; margin-right: 8px" /><span class="channel">查看历史</span>
              </a>
            </li>
            
          </ul>
        </div>
        <div class="main-content with-side-bar">
          <router-view />
        </div>
      </div>
      <div class="edit-profile">
        <el-dialog v-model="editVisible" title="编辑个人信息"  style="width:500px; z-index:100">
          <el-form :model="form_edit"  label-width="auto"  @submit.prevent="saveEdit">
            <el-form-item label="用户名">
              <el-input v-model="form_edit.name"></el-input>
            </el-form-item>
            <el-form-item label="邮箱">
              <el-input v-model="form_edit.add"></el-input>
            </el-form-item>
            <el-form-item label="密码">
              <el-input v-model="form_edit.password"></el-input>
            </el-form-item>            
            <el-form-item>
              <el-button type="primary" native-type="submit">保存</el-button>
              <el-button @click="editVisible = false">取消</el-button>
            </el-form-item>
          </el-form>
        </el-dialog>
      </div>
    </div>
  </template>
  
<script setup>
    import {
      House,   
      DataAnalysis,
      User,
      Calendar,
      ArrowDown,
      MapLocation,
    } from "@element-plus/icons-vue";
    import { useRouter } from "vue-router";
    import { ref, onMounted } from "vue";
    import store from "../../store/index";
    import axios from "axios";
    
    const router = useRouter();
    const activeChannel = ref('manage');
    const userId = store.state.user_id;
    const username = ref();
    const useradd = ref();
    const userpassword = ref();
    const editVisible = ref(false);
    const form_edit=ref({});

    const getUserName = async () => {
      const response = await axios.get(`/get_user/${userId}`);
      const result = response.data;
      // 解构出各个属性数组
      username.value=result.username;
      useradd.value=result.add;
      userpassword.value=result.password;
    };

    
    const toManage = () => {
      router.push({ name: 'manage' });
      activeChannel.value = 'manage';
    };
    const toAnalysis = () => {
      // console.log("toAnalysis");
      // router.push({ name: 'analysis' });
      activeChannel.value = 'analysis';
    };
    const toCharts = () => {
      // console.log("toAnalysis");
      router.push({ name: 'analysis' });
      activeChannel.value = 'charts';
    };
    const toUserManage = () => {
      router.push({ name: 'userManage' });
      activeChannel.value = 'userManage';
    };
    const toHistory = () => {
      router.push({ name: 'history' });
      activeChannel.value = 'history';
    };
    const toMap = () => {
      router.push({ name: 'map' });
      activeChannel.value = 'map';
    };
    const handleEdit = (index, row) => {
      // console.log(index, row);
      // form_edit.value = { ...row };
      form_edit.value.name = username.value;
      form_edit.value.add = useradd.value;
      form_edit.value.password = userpassword.value;
      editVisible.value = true;
    };
    
    const saveEdit = async () => {
    try {
      console.log('form_edit');
      console.log(form_edit.value.id);
      const response = await axios.post(`/edit_user`, 
      {
        user_id: userId,
        username: form_edit.value.name,
        add: form_edit.value.add,
        password: form_edit.value.password 
      },
      {
          headers: {
              'Content-Type': 'application/json'
          }
      });
      username.value=form_edit.value.name;  
      useradd.value=form_edit.value.add;
      userpassword.value=form_edit.value.password;    
      console.log(response);
      editVisible.value = false;
      form_edit.value = {};
    } catch (error) {
      console.error('Error editing data:', error);
    }
  }
    
    // const toggleMoreInfoState = () => {
    //   let div = document.getElementById('more-info');
    //   if (div.style.visibility === 'hidden') {
    //     div.style.visibility = 'visible';
    //   } else {
    //     div.style.visibility = 'hidden';
    //   }
    // }
    
    function Logout(){
      store.commit("setLoginState",false);
      store.commit("setCurUserID",null);
      store.commit('setAdminState', false);
      localStorage.removeItem("user");
      localStorage.removeItem("is_admin");
      router.push("/");
    }
    // 保存到本地，这样不需要每次刷新都得登录
    store.commit("setLoginState",localStorage.getItem("user")?true:false);
    store.commit("setCurUserID",localStorage.getItem("user")?localStorage.getItem("user"):null);
    store.commit("setAdminState",localStorage.getItem("is_admin")?localStorage.getItem("is_admin"):null);

    onMounted(() => {
      getUserName();
    });
</script>
  
<style lang="less" scoped>
  .icon-hover {
    cursor: pointer; /* 使鼠标悬浮时变为手型 */
    transition: transform 0.3s ease; /* 过渡效果，可以添加其他视觉效果，如轻微放大 */
  }
  
  .icon-hover:hover {
    transform: scale(1.1); /* 轻微放大图标 */
  }
  
  
  .sub-menu {
    padding-left: 20px;  /* 保持适当的缩进 */
    background-color: rgba(255, 255, 255, 0);
    border-radius:  999px;;
    margin-top: 0px;
    min-height: 48px; 
    
  }
  
  .channel-list > li {
    position: relative;  /* 确保设置了定位上下文 */
  }
  
  .sub-menu li {
    padding: 8px 16px;  /* 子菜单项的内边距 */
    white-space: nowrap;  /* 防止文本换行 */
    cursor: pointer;
    height: 40px;  /* Explicit height for each submenu item */
  }
  
  .sub-menu li:hover {
    background-color:  rgba(0, 0, 0, 0.03);
    border-radius: 999px;
    
  }
  
  .container {
    max-width: 1728px;
    background-color: rgba(201, 19, 19, 0);
    margin: 0 auto;
    height:100%;
  
    .top {
      display: flex;
      flex-direction: column;
      // justify-content: center;
      width: 100vw;
      height: 51px;
      position: fixed;
      left: 0;
      top: 0;
      z-index: 30;
      // align-items: center;
      background: #fff;
      // border-color: #333;
      border-bottom: 1px solid #e8e8e8;
  
      header {
        position: relative;
        display: flex;
        align-items: center;
        // justify-content: space-between;
        width: 100%;
        max-width: 1728px;
        height: 50px;
        padding: 0 16px 0 24px;
        z-index: 10;
        .logo {
          cursor: pointer;  /* 设置鼠标为手形指针 */
          width:4.2%;
          position: relative; 
          top:0px; 
          left:0px; 
        }
        .welcome{
          position: relative;
          font-size: 22px;
          font-weight: 600;
          color: #333;
          left: 10px;
          
        }
        .downbar{
          cursor: pointer;
          position: absolute;
          font-size: 22px;
          font-weight: 600;
          color: #7a7a7a;
          top: 17px;
          right: 50px;
        }
  
        .input-box {
          height: 40px;
          position: fixed;
          left: 50%;
          transform: translate(-50%);
  
          @media screen and (max-width: 695px) {
            display: none;
          }
  
          @media screen and (min-width: 960px) and (max-width: 1191px) {
            width: calc(-36px + 50vw);
          }
  
          @media screen and (min-width: 1192px) and (max-width: 1423px) {
            width: calc(-33.6px + 40vw);
          }
  
          @media screen and (min-width: 1424px) and (max-width: 1727px) {
            width: calc(-42.66667px + 33.33333vw);
          }
  
          @media screen and (min-width: 1728px) {
            width: 533.33333px;
          }
          .search-input {
            padding: 0 84px 0 16px;
            width: 100%;
            height: 100%;
            font-size: 16px;
            line-height: 120%;
            color: #333;
            caret-color: #ff2442;
            background: rgba(0, 0, 0, 0.03);
            border-radius: 999px;
          }
  
          .input-button {
            position: absolute;
            right: 0;
            top: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100%;
            color: rgba(51, 51, 51, 0.8);
  
            .close-icon .search-icon {
              width: 40px;
              height: 100%;
              display: flex;
              align-items: center;
              justify-content: center;
              cursor: pointer;
              color: rgba(51, 51, 51, 0.8);
            }
          }
        }
      }
    }
  
    .main {
      display: flex;
      width:100%;
  
      .side-bar {
        @media screen and (max-width: 695px) {
          display: none;
        }
        @media screen and (min-width: 696px) and (max-width: 959px) {
          display: none;
        }
  
        @media screen and (min-width: 960px) and (max-width: 1191px) {
          width: calc(-18px + 22vw);
          // margin-left: 12px;
        }
  
        @media screen and (min-width: 1192px) and (max-width: 1423px) {
          width: calc(-16.8px + 15vw);
          // margin-left: 12px;
        }
  
        @media screen and (min-width: 1424px) and (max-width: 1727px) {
          width: calc(-21.33333px + 11.66667vw);
          // margin-left: 16px;
        }
  
        @media screen and (min-width: 1728px) {
          width: 200px;
          // margin-left: 16px;
        }
  
        height: calc(100vh - 50px);
        width:100px;

        overflow-y: scroll;
        background-color: #fff;
        display: flex;
        flex-direction: column;
        flex-shrink: 0;
        padding-top: 16px;
        margin-top: 50px;
        left:0;
        position: fixed;
        overflow: visible;
  
        .channel-list > li {
          position: relative;  /* Ensuring that the positioning context is set */
        }
  
        .channel-list {
          min-height: auto;
          -webkit-user-select: none;
          user-select: none;
          
  
          .active-channel {
            background-color: rgba(213,238,250);//rgba(60, 139, 185, 0.03);
            // border-radius: 999px;
            color: #333;
          }
  
          li {
            padding-left: 12px;
            min-height: 48px;
            display: flex;
            align-items: center;
            cursor: pointer;
            margin-bottom: 8px;
            color: rgba(51, 51, 51, 0.6);
  
            .link-wrapper {
              display: flex;
              width: 100%;
              height: 48px;
              align-items: center;
              text-decoration: none;
            }
          }
  
          .channel {
            font-size: 16px;
            font-weight: 600;
            margin-left: 12px;
            color: #333;
            white-space: nowrap;  /* 防止文本换行 */
          }
        }
  
        .information-container {
          display: inline-block;
          width: 100%;
          color: #333;
          font-size: 16px;
          position: absolute;
          bottom: 0;
  
          .information-pad {
            z-index: 16;
            margin-bottom: 4px;
            width: 100%;
  
            .container {
              width: 100%;
              background: #fff;
              box-shadow:
                0 4px 32px 0 rgba(0, 0, 0, 0.08),
                0 1px 4px 0 rgba(0, 0, 0, 0.04);
              border-radius: 12px;
  
              .divider {
                margin: 0px 12px;
                list-style: none;
                height: 0;
                border: 1px solid rgba(0, 0, 0, 0.08);
                border-width: 1px 0 0;
              }
  
              .group-wrapper {
                padding: 4px;
  
                .group-header {
                  display: flex;
                  align-items: center;
                  padding: 0 12px;
                  font-weight: 400;
                  height: 32px;
                  color: rgba(51, 51, 51, 0.6);
                  font-size: 12px;
                }
  
                .menu-item {
                  height: 40px;
                  color: rgba(51, 51, 51, 0.8);
                  font-size: 16px;
                  border-radius: 8px;
                  display: flex;
                  align-items: center;
                  padding: 0 12px;
                  font-weight: 400;
  
                  .icon {
                    color: rgba(51, 51, 51, 0.3);
                    margin-left: auto;
                  }
  
                  .component {
                    margin-left: auto;
                  }
  
                  .multistage-toggle {
                    position: relative;
                    background: rgba(0, 0, 0, 0.03);
                    display: flex;
                    padding: 2px;
                    border-radius: 999px;
                    cursor: pointer;
  
                    .active {
                      background: #fff;
                      box-shadow:
                        0 2px 8px 0 rgba(0, 0, 0, 0.04),
                        0 1px 2px 0 rgba(0, 0, 0, 0.02);
                      color: #333;
                    }
  
                    .toggle-item {
                      border-radius: 999px;
                      background: transparent;
                      color: rgba(51, 51, 51, 0.6);
  
                      .icon-wrapper {
                        width: 24px;
                        height: 24px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        cursor: pointer;
                      }
                    }
                  }
                }
              }
            }
          }
  
          .information-wrapper {
            -webkit-user-select: none;
            user-select: none;
            cursor: pointer;
            position: relative;
            margin-bottom: 20px;
            height: 48px;
            width: 100%;
            display: flex;
            font-weight: 600;
            align-items: center;
            border-radius: 999px;
            padding: 0 16px;
          }
        }
      }
  
      .main-content {
        width: 100%;
      }
  
      .main-content {
        @media screen and (max-width: 695px) {
          display: none;
        }
        @media screen and (min-width: 696px) and (max-width: 959px) {
          display: none;
        }
  
        @media screen and (min-width: 960px) and (max-width: 1191px) {
          width: calc(-18px + 22vw);
          // margin-left: 12px;
        }
  
        @media screen and (min-width: 1192px) and (max-width: 1423px) {
          width: calc(-16.8px + 15vw);
          // margin-left: 12px;
        }
  
        @media screen and (min-width: 1424px) and (max-width: 1727px) {
          width: calc(-21.33333px + 11.66667vw);
          // margin-left: 16px;
        }
  
        @media screen and (min-width: 1728px) {
          width: 500px;
          // margin-left: 16px;
        }
      }
      .main-content.with-side-bar {
        // width:100%;
        width:1010px;
      }
    }
  }
</style>
  
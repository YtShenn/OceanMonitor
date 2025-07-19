<template>
  <div>
    <div id="container"></div>
  </div>
</template>


<script setup>
  import AMapLoader from '@amap/amap-jsapi-loader';
  import { onMounted,ref } from 'vue';
  import axios from 'axios';
  import * as echarts from 'echarts';
  var map=null;
  const Data = ref([]);


  const initMap = () => {
    AMapLoader.load({
      key: "ab0fd16f15427db830906040d6b4d3f0", //此处填入我们注册账号后获取的Key
      version: "2.0", //指定要加载的 JSAPI 的版本，缺省时默认为 1.4.15
      plugins: [''], //需要使用的的插件列表，如比例尺'AMap.Scale'等
    }).then((AMap) => {
      map = new AMap.Map("container", { //设置地图容器id
        viewMode: "3D", //是否为3D地图模式
        zoom: 5, //初始化地图级别
        center:[122,30],// [105.602725, 37.076636], //初始化地图中心点位置
      });
    }).catch(e => {
      console.log(e);
    })
  }

  const getData = async ()=>{
    const response = await axios.get(`/get_table`);
    Data.value = response.data.dataList;
    showPoint();
  }

  const showPoint=()=>{
    //获取Data中的数据的个数
    var num = Data.value.length; 
    console.log("Data.value");
    console.log(num);
    //按照Data中的lat和lon分组，将相同的lat和lon的数据放在一个列表中
    const group = Data.value.reduce((acc, cur) => {
        const key = `${cur.lon},${cur.lat}`;
        console.log("key");
        console.log(key);
        if (!acc[key]) {
            acc[key] = [];
        }
        acc[key].push(cur);
        return acc;
    }, {});
    console.log("group");
    console.log(group);
    var infoWindowOpen = Array(group.length).fill(false);
    Object.keys(group).forEach((key) => {
      //获取key的索引
      var i = Object.keys(group).indexOf(key);
      var infoWindow = new AMap.InfoWindow({
            isCustom: true,
            draggable: false,  //是否可拖动
            offset: new AMap.Pixel(0, -31),
            content: ""
        });
        console.log("group[key]");
        console.log(group[key]);

      const [lon, lat] = key.split(',');
      const center = [lon, lat];      
      var circleMarker = new AMap.CircleMarker({
          center:center,
          radius:10+Math.random()*10,//3D视图下，CircleMarker半径不要超过64px
          strokeColor:'white',
          strokeWeight:2,
          strokeOpacity:0.5,
          fillColor:'rgba(0,0,255,1)',
          fillOpacity:0.5,
          zIndex:10,
          bubble:true,
          cursor:'pointer',
          clickable: true
        });
        circleMarker.setMap(map);

        // circleMarker.index = i;
        //单击风力标点触发显示窗体
        circleMarker.on('click', (e) => {
          // 根据e添加的index信息获取circleMarker对象
          console.log(e.target.index);
          var idx = e.target.index;
          if(infoWindowOpen[idx]){
            infoWindow.close();
            infoWindowOpen[idx] = false;
          }
          else{         
            infoWindow.setContent(
                "<div class='power_window'>"
                    +"<div class='left_wind'>"
                      +"<span> 经度："+lon+'</span>'
                      +"<span> 纬度："+lat +'</span>'
                      +"</div>"
                      +"<div class='right_charts'>"
                      // +"<div class='chart-container'>"
                      +"<div id='line' class='chart'></div>"
                      +"<div id='line2' class='chart'></div>"
                      +"</div>"
                +"</div>"
                );
            infoWindow.open(map, e.lnglat);
            // 创建折线图
            const line = echarts.init(document.getElementById('line'));
            line.setOption({
              grid: {
                  top: '15%',    // 设置上边距为10%
                  bottom: '30%', // 设置下边距为10%
                },
                title: {
                  text: '海水温度',
                  textStyle: {
                    fontSize: 13, // Set the desired font size here
                  },
                  padding: [, 0, 0, 0], // Set the desired padding here
                },
                tooltip: {trigger: 'axis'},
                xAxis: {
                  data: group[key].map(item => item.date),
                  axisLabel: {
                    interval: 0,
                    rotate: 45,
                    textStyle: {
                      fontSize: 8, // Set the desired font size here
                    },
                  }
                },

                yAxis: {},
                series: [{
                data: group[key].map(item => item.temp),
                type: 'line'
                }]
            });

            const line2 = echarts.init(document.getElementById('line2'));
            line2.setOption({
              grid: {
                  top: '15%',    // 设置上边距为10%
                  bottom: '30%', // 设置下边距为10%
                },
                title: {
                  text: '海平面高度',
                  textStyle: {
                    fontSize: 13, // Set the desired font size here
                  },
                  padding: [0, 0, 0, 0], // Set the desired padding here
                },
                tooltip: {trigger: 'axis'},
                xAxis: {
                  data: group[key].map(item => item.date),
                  axisLabel: {
                    interval: 0,
                    rotate: 45,
                    textStyle: {
                      fontSize: 8, // Set the desired font size here
                    },
                  }
                },

                yAxis: {},
                series: [{
                data: group[key].map(item => item.sl),
                type: 'line'
                }]
            });
            infoWindowOpen[idx] = true;
          }
        });
      
    });
  }

  onMounted(() => {
    initMap();
    getData();
    // showPoint();
  })

</script>
 
<style>
  #container {
    width: 1195px;
    height:735px;
    /* margin: 100px auto; */
    margin-top: 50px;
    margin-left: 170px;
    /* border: 1px solid red; */
  }
  .power_window{
    background-color: rgb(255, 255, 255);
    width:400px;
    height:300px;
    border-radius: 20px;
    display: flex;
    flex-direction: row;
  }
  .left_wind{
    position: relative;
    display: flex !important;
    flex-direction: column !important;
    height:100%;
    width:35%;  
    border-top-left-radius: 20px;
    border-bottom-left-radius: 20px;
    background-color: rgb(255, 129, 129);
    color: rgb(255, 255, 255);
    font-size: 20px;
    font-weight: 800;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    padding:10px;
  }
  .left_wind span {
    display: block;
    margin-bottom:5px;
    margin-top:5px;
  }
  .chart{
    display: block;
        position:relative;
        /* top:20px; */
        /* top:50px; */
        /* left:-30px; */
        width: calc(100% - 30px);
        /* width:100%; */
        height:130px; 
        margin-left: 20px;
        /* margin-bottom:10px; */
        /* margin-top:10px; */
        /* padding:10px; */
        /* margin-right: 50px; */
    }
    .right_charts{
      position: relative;
      display: flex !important;
      flex-direction: column !important;
      justify-content: space-around !important;
      height:100%;
      width:65%; 
      /* padding:10px;  */
      /* border-top-left-radius: 20px;
      border-bottom-left-radius: 20px;
      background-color: rgb(255, 129, 129);
      color: rgb(255, 255, 255);
      font-size: 20px;
      font-weight: 800;
      display: flex;
      flex-direction: row;
      justify-content: center;
      align-items: center;
      padding:10px; */
  }
</style>
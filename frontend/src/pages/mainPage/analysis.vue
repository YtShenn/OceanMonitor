<template>
    <div class="top_info">
        <div class="title">数据分析</div>
        <div>
            <el-cascader :options="options" :props="props1" clearable @change="handleCascader"/>
            <span class="note">分析方式</span>
        </div>
        <div>
            <el-button type="success" @click="Predict" :disabled="cascade_value==undefined || cascade_value[0]==null|| cascade_value[0] == 'date'">预测</el-button>
        </div>
        <div>
            <el-radio-group v-model="radio">
                <el-radio-button label="水温" value="temp" @click="drawCharts"/>
                <el-radio-button label="海平面" value="sea_level" @click="drawCharts"/>
            </el-radio-group>
        </div>
    </div>
    <div class="container">
        <div class="chart-container">
            <div id="scatter" class="chart"></div>
        </div>
        <div class="chart-container">
            <div id="bar" class="chart"></div>
        </div>
        <div class="chart-container">
            <div id="pie" class="chart"></div>
        </div>
        <div class="chart-container">
            <div id="line" class="chart"></div>
        </div>
        
    </div>
    
    <el-dialog v-model="showResult" class="predict" width="1000px">
        <div style="display: flex; font-size: 16px;
      font-weight: 600; justify-content: center; align-items: center;">
            <span>预测结果为：在 </span>
            <span style="color:red">{{predict_time}}</span>
            <span> 时的水温为</span>
            <span style="color:red">{{predict_temp}}</span>
            <span>℃，海平面高度为</span>
            <span style="color:red">{{predict_sea_level}}</span>
        </div>
        <div style="display:flex">
            <div class="chart-container2">
                <div ref="chartDom" class="chart2"></div>
            </div>
            <div class="chart-container2">
                <div ref="chartDom2" class="chart2"></div>
            </div>
        </div>
    </el-dialog>
</template>

<script setup>
    import axios from "axios";
    import * as echarts from 'echarts';
    import {onMounted, ref, watch,nextTick} from 'vue';
    
    const props1 = { checkStrictly: true, }
    const data_ = ref([]);
    const data2_t = ref([]);
    const data2_s = ref([]);
    const options = ref([
        {
            value: 'pos',
            label: '按位置',
            children:[],
        },
        {
            value: 'date',
            label: '按时间',
            children: [],
        }
    ]);
    const cascade_value=ref({});
    console.log("cascade_value.value");
    console.log(cascade_value.value);
    const radio = ref('temp');
    watch(radio, (newVal) => {
        drawCharts(newVal);
    });
    const showResult = ref(false);
    const predict_time = ref(0);
    const predict_temp = ref(0);
    const predict_sea_level = ref(0);
    const chartDom = ref(null);
    const chartDom2 = ref(null);

    const drawCharts = async (newRadioValue) => {
        // var response={};
        console.log(newRadioValue);
        if(cascade_value.value==undefined||cascade_value.value[0]==null||cascade_value.value[1]==null) return;
        if (newRadioValue == 'temp') {            
            if(cascade_value.value[0]=='pos'){
                const num=cascade_value.value[1];
                const response = await axios.get(`/draw_data_temp_pos/${num}`);
                data_.value = response.data.data;
            }
            else{
                const num=cascade_value.value[1];
                const response = await axios.get(`/draw_data_temp_date/${num}`);
                data_.value = response.data.data;
            }
            
        } else {
            if(cascade_value.value[0]=='pos'){
                const num=cascade_value.value[1];
                const response = await axios.get(`/draw_data_sea_level_pos/${num}`);
                data_.value = response.data.data;
            }
            else{
                const num=cascade_value.value[1];
                const response = await axios.get(`/draw_data_sea_level_date/${num}`);
                data_.value = response.data.data;
            }
            // const response = await axios.get('/draw_data_sea_level');
            // data_.value = response.data.data;
        }
        // const response = await axios.get('/draw_data_temp');
        // console.log(response.data);
        // const data = response.data.data;
        const data = data_.value;
        data.sort((a, b) => new Date(a.name) - new Date(b.name));

        // 创建散点图
        const scatter = echarts.init(document.getElementById('scatter')); 
        scatter.setOption({
            tooltip: {trigger: 'axis'},
            title: {text: '散点图'},
            xAxis: {data: data.map(item => item.name)},
            yAxis: {},
            series: [{
                symbolSize: 20,
                data: data.map(item => [item.name, item.value]),
                type: 'scatter',
                
            }]
        });
    

        // 创建条形图
        const bar = echarts.init(document.getElementById('bar'));
        bar.setOption({
            title: {text: '柱状图'},
            tooltip: {trigger: 'axis'},
            xAxis: {
            data: data.map(item => item.name)
            },
            yAxis: {},
            series: [{
            data: data.map(item => item.value),
            type: 'bar'
            }]
        });

        // 创建饼状图
        const pie = echarts.init(document.getElementById('pie'));
        pie.setOption({
            title: {text: '饼状图'},
            // legend: {data: data.map(item => item.name)},
            tooltip: {trigger: 'item'},
            series: [{
            data: data,
            type: 'pie'
            }]
        });

        // 创建折线图
        const line = echarts.init(document.getElementById('line'));
        line.setOption({
            title: {text: '折线图'},
            tooltip: {trigger: 'axis'},
            xAxis: {
            data: data.map(item => item.name)
            },
            yAxis: {},
            series: [{
            data: data.map(item => item.value),
            type: 'line'
            }]
        });
    };

    const get_pos = async () => {
        const response = await axios.get('/api/get_pos_key');
        const keys = response.data.map(item => ({value:item,label:item})); 
        console.log(keys);
        options.value.find(option => option.value === 'pos').children = keys;
        console.log(options.value);
    };
    const get_date = async () => {
        const response = await axios.get('/api/get_date_key');
        const keys = response.data.map(item => ({value:item,label:item})); 
        options.value.find(option => option.value === 'date').children = keys;
    };
    const handleCascader  = async (value) =>{
      console.log('选中的值:', value);
      cascade_value.value = value;
      drawCharts(radio.value);
    }
    const Predict = async () => {
        const num=cascade_value.value[1];
        const response = await axios.get(`/predict/${num}`);
        predict_time.value = response.data.new_date;
        predict_temp.value = response.data.pred_temp;
        predict_sea_level.value = response.data.pred_sl;

        console.log(response.data);
        data2_t.value = response.data.data_temp;
        data2_t.value.sort((a, b) => new Date(a.name) - new Date(b.name));
        data2_s.value = response.data.data_sl;
        data2_s.value.sort((a, b) => new Date(a.name) - new Date(b.name));
        
        showResult.value = true;
        await nextTick();

        const line = echarts.init(chartDom.value);
        line.setOption({
            title: {text: '预测海温'},
            tooltip: {trigger: 'axis'},
            xAxis: {
                data: data2_t.value.map(item => item.name),
                axisLabel: {
                    interval: 0,  // 设置为 0 表示每个单位都显示
                    rotate: 45,   // 旋转角度
                }
            },
            yAxis: {},
                series: [{
                data: data2_t.value.map(item => item.value),
                type: 'line',
                itemStyle: {
                    color: (params) => {
                        // 如果是最后一个数据点，返回红色，否则返回默认颜色
                        return params.dataIndex === data2_t.value.length - 1 ? 'red' : '#5470C6';
                    }
                }
            }]
        });

        const line2 = echarts.init(chartDom2.value);
        line2.setOption({
            title: {text: '预测海平面'},
            tooltip: {trigger: 'axis'},
            xAxis: {
                data: data2_s.value.map(item => item.name),
                axisLabel: {
                    interval: 0,  // 设置为 0 表示每个单位都显示
                    rotate: 45,   // 旋转角度
                }
            },
            yAxis: {},
                series: [{
                data: data2_s.value.map(item => item.value),
                type: 'line',
                itemStyle: {
                    color: (params) => {
                        // 如果是最后一个数据点，返回红色，否则返回默认颜色
                        return params.dataIndex === data2_s.value.length - 1 ? 'red' : '#5470C6';
                    }
                }
            }]
        });
    }

    onMounted(() => {
        radio.value = 'temp';
        if(cascade_value.value!=undefined){
            drawCharts(radio.value);
        }
        get_pos();
        get_date();
    });

</script>

<style scoped>
    
    .el-dialog{
        height:850px;
        width:800px !important;
    }
    .container {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-around;

        
        
    }
    .chart-container{
        position:relative;
        top:20px;
        left:260px;
        width: calc(50% - 80px);
        height:300px; 
        background-color: white;
        border-radius: 10px;
        border-color: #d3d1d1;
        border-width: 1px;
        /* border-style: solid; Add this line to set the border style */
        padding: 20px;
        margin-bottom:20px;
        margin-left:30px;
        margin-right:30px;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1); /* Add this line to add box shadow */
    }

    .chart{
        position:relative;
        /* top:50px; */
        left:-30px;
        width: calc(100% - 30px);
        width:100%;
        height:300px; 
        margin-left: 50px;
        margin-right: 50px;
    }
    .chart-container2{
        position:relative;
        top:20px;
        width: calc(45%);
        height:380px; 
        background-color: white;
        border-radius: 10px;
        border-color: #d3d1d1;
        border-width: 1px;
        /* border-style: solid; Add this line to set the border style */
        padding: 20px;
        margin-bottom:20px;
        margin-left:30px;
        margin-right:10px;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1); /* Add this line to add box shadow */
    }

    .chart2{
        position:relative;
        /* top:50px; */
        left:-30px;
        /* width: calc(100% - 30px); */
        width:100%;
        height:350px; 
        margin-left: 50px;
        
        margin-bottom:15px;
        margin-right: 50px;
    }
    .table{
        position: relative;
        /* padding-top: 65px;
        padding-left: -100px; */
        margin-left: 200px;
        margin-top: 20px;
        width:1150px;
    }
  .top_info{
    width: 100%;
    position: relative;
    display: flex;
    /* grid-auto-flow: column; */
    margin-top: 70px;
    margin-left: 230px;
    justify-content: space-between;

    .title{
      position: relative;
      font-size: 20px;
      font-weight: 600;
      color: #333;
      width: 100px;
    }
    .note{
      position: relative;
      font-size: 16px;
      font-weight: 550;
      color: #6b6b6b;
      width: 100px;
      margin-left: 10px;
    }
  }
</style>
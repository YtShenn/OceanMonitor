<template>
    <div class="top_info">
      <div class="title">用户管理</div>
      <!-- <el-button type="success" @click="showDialog = true">添加</el-button> -->
      <el-input v-model="searchQuery" placeholder="Search..." style="width: 200px;">
        <template #suffix>
          <el-icon>
            <Search />
          </el-icon>
        </template>
      </el-input>
     
      
      
    </div>
    <div class="cards">
      <el-row :gutter="10">
        <el-col :span="4.5" v-for="user in users_" :key="user.id">
          <el-card shadow="hover" style="margin-bottom: 20px;">
            <!-- <div slot="header" class="clearfix">
              <span>{{ user.username }}</span>
              <el-button type="text" @click="deleteUser(user.id)" icon="el-icon-close"></el-button>
            </div> -->
            <template #header class="clearfix">
              <div class="card-header" style="display: flex; justify-content: space-between;">
                <div style="text-align: center;">{{user.username}}</div>
                <!-- <div style="width: 60px; display: inline-block;"></div>  占位符 -->
                <el-button type="danger" text @click="deleteUser(user.id)">删除</el-button>
              </div>
            </template>
            <p>用户ID: {{ user.id }}</p>
            <p>角色: {{ user.role }}</p>
            <p>邮箱: {{ user.add }}</p>
            <p>密码: {{ user.password }}</p>
            <!-- 其他用户信息字段 -->
          </el-card>
        </el-col>
      </el-row>
    </div>
  </template>
  
  <script setup>
    import { Search } from "@element-plus/icons-vue";
    import { ref, onMounted, reactive, toRaw, computed } from "vue";
    import store from "../../store/index";
    import axios from "axios";
  // import { id } from "element-plus/es/locale";
    // import { id } from "element-plus/es/locale";
    const headerCellStyle = { background: '#f7f7f7', color: '#333', fontWeight: 'bold', textAlign: 'center' };
    const cellStyle = { textAlign: 'center' };
  
    //===变量定义======================================================
    const tableData = ref([]);
    const searchQuery = ref('');
    const users = ref([]);
  
    console.log(searchQuery.value);
    const users_ = computed(() =>
      users.value.filter(
      //   (data)=>Object.values(data).some((value) =>
      //   value.toString().toLowerCase().includes(searchQuery.value.toLowerCase())
      // )
      (data)=>(!searchQuery.value || data.username.toString().toLowerCase().includes(searchQuery.value.toLowerCase()))
                  
    ));
    const userId = store.state.user_id;
    
    //===函数定义======================================================
    const fetchData = async () => {
      const response = await axios.get(`/get_all_user`);
      users.value = response.data.dataList;
      console.log(users.value);
    };
  
    const addInfo= async () => {
      try {
        console.log("vye=================");
        console.log(form.lon);
        const response = await axios.post(`/add_info`, form,{
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        });
        console.log(response);
        tableData.value.push({
          id : response.data.id,
          pos: response.data.pos,
          lon: form.lon,
          lat: form.lat,
          date: response.data.time,
          temp: form.temp,
          sl: form.sl,
          user_id: userId,
        });
        showDialog.value = false;
        form.value = { 
          // pos: '',
          lon: '',
          lat: '',
          date1: '',
          date2: '',
          temp: '',
          sl: '',};
      } catch (error) {
        console.error('Error adding data:', error);
      }
    };
  
    
    const deleteUser = async (userid) => {
      try {
       
        const response = await axios.get(`/delete_user/${userid}`, {headers: {
                'Content-Type': 'application/json'
            }});
        // Remove the row from the table
        // tableData.value.splice(index, 1);
        //在users中删除对应的用户
        users.value = users.value.filter(user => user.id !== userid);
      } catch (error) {
        console.error('Error deleting data:', error);
      }
    }
  
    onMounted(() => {
      fetchData();
    });
  </script>
  
  <style scoped>
   
    .cards{
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
    }
    .el-dialog__body {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .dialog-footer {
    text-align: right;
  }
  ::v-deep .card-header{
    font-size: 16px;
    font-weight: 600;
    padding:0rem 0rem;
    margin-bottom: 0;
    background-color: #fff;
    border-bottom: none;
    text-align: center;
  }
  .el-card{
    width:220px;
  }
  </style>
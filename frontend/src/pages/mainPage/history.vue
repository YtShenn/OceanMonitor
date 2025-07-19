<template>
    <div class="top_info">
      <div class="title">编辑历史</div>
      <el-input v-model="searchQuery" placeholder="Search..." style="width: 200px;">
        <template #suffix>
          <el-icon>
            <Search />
          </el-icon>
        </template>
      </el-input>
      <!-- <template #header>
        <el-input v-model="search" size="small" placeholder="Type to search" />
      </template> -->
      <el-select v-model="selectedColumn" placeholder="Select Column" style="width: 200px;">
        <el-option
          v-for="column in columns"
          :key="column.value"
          :label="column.label"
          :value="column.value"
        ></el-option>
      </el-select>
      <!-- <el-button type="primary" @click="filterTable">Search</el-button>    -->
      
      
    </div>
    <div class="table">
      <el-table :data="filterTableData" stripe style="width: 100%" :header-cell-style="headerCellStyle"
      :cell-style="cellStyle" :table-layout="tableLayout" :size="300">
        <el-table-column prop="id" label="id" min-width="80px"/>
        <el-table-column prop="date" label="编辑时间" min-width="100px"/>
        <el-table-column prop="info_id" label="信息编号" min-width="80px"/>
        <el-table-column prop="user_id" label="编辑人员" min-width="80px"/>
        <el-table-column prop="content" label="编辑内容" min-width="400px"/>
        <!-- <el-table-column prop="op" label="操作" min-width="200px"/> -->
        <el-table-column align="right" prop="op" label="操作" min-width="80px">       
          <template #default="scope">
            <el-button
              size="small"
              type="danger"
              @click="handleDelete(scope.$index, scope.row)"
            >
              Delete
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </template>
  
  <script setup>
    import { Search } from "@element-plus/icons-vue";
    import { ref, onMounted, reactive, toRaw, computed } from "vue";
    import store from "../../store/index";
    import axios from "axios";
    const headerCellStyle = { background: '#f7f7f7', color: '#333', fontWeight: 'bold', textAlign: 'center' };
    const cellStyle = { textAlign: 'center' };
  
    //===变量定义======================================================
    const tableData = ref([]);
    const searchQuery = ref('');
    const userId = store.state.user_id;    
    const editVisible = ref(false);
    const selectedColumn = ref('');
    const columns = [
    {
      value: 'id',
      label: 'id',
    },
    {
      value: 'date',
      label: '编辑时间',
    },
    {
      value: 'info_id',
      label: '信息编号',
    },
    {
      value: 'user_id',
      label: '编辑人员',
    },
    {
      value: 'content',
      label: '编辑内容',
    },
    
  ];
    
  console.log(searchQuery.value);
  console.log('selectedColumn.value');
  console.log(selectedColumn.value);
  const filterTableData = computed(() =>
    tableData.value.filter(
      (data) =>{
          if (!searchQuery.value) {
              // 如果 searchQuery 为空，返回所有数据
              return true;
          } 
          else if (selectedColumn.value == '') {
              // 如果 selectedColumn 为 undefined，遍历 data 的每个属性
              return Object.values(data).some((value) =>
              value.toString().toLowerCase().includes(searchQuery.value.toLowerCase())
          );
          } else {
          // 否则，只在 selectedColumn 列中搜索
              return data[selectedColumn.value]
                  .toString()
                  .toLowerCase()
                  .includes(searchQuery.value.toLowerCase());
          }
      }
    )
  )
  
  console.log('selectedColumn');
  console.log(selectedColumn.value);
    
    
    //===函数定义======================================================
    const fetchData = async () => {
      const response = await axios.get(`/get_history`);
      tableData.value = response.data.dataList;
      console.log(tableData.value);
    };

    const handleDelete = async (index, row) => {
      try {
        // Send a DELETE request to the backend
        console.log(index, row);
        //把row转换为json格式
        const row_json = JSON.stringify(toRaw(row));
        console.log(row_json);
        // console.log(tableData.value[index]);
        const response = await axios.post(`/delete_history`, row_json, {headers: {
                'Content-Type': 'application/json'
            }});
        // Remove the row from the table
        tableData.value.splice(index, 1);
      } catch (error) {
        console.error('Error deleting data:', error);
      }
    }
  
    onMounted(() => {
      fetchData();
    });
  </script>
  
  <style scoped>
   
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
    }
    .el-dialog__body {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .dialog-footer {
    text-align: right;
  }
  </style>
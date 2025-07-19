<template>
  <div class="top_info">
    <div class="title">海水信息</div>
    <el-button type="success" @click="showDialog = true">添加</el-button>
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
      <el-table-column prop="pos" label="采样点" min-width="80px"/>
      <el-table-column prop="lon" label="经度" min-width="80px"/>
      <el-table-column prop="lat" label="纬度" min-width="80px"/>
      <el-table-column prop="date" label="采样时间" min-width="160px"/>
      <el-table-column prop="temp" label="海水温度" min-width="120px"/>
      <el-table-column prop="sl" label="海平面高度" min-width="120px"/>
      <el-table-column prop="user_id" label="录入人员" min-width="100px"/>
      <!-- <el-table-column prop="op" label="操作" min-width="200px"/> -->
      <el-table-column align="right" prop="op" label="操作" min-width="200px">       
        <template #default="scope">
          <el-button size="small" @click="handleEdit(scope.$index, scope.row)">
            Edit
          </el-button>
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


  <el-dialog title="添加数据" v-model="showDialog" style="width:500px; z-index:100">
    <el-form :model="form" label-width="auto"  @submit.prevent="addInfo">
      <!-- <el-form-item label="采样点">
        <el-input v-model="form.defineProps"></el-input>
      </el-form-item> -->
      <el-form-item label="经度">
        <el-input v-model="form.lon"></el-input>
      </el-form-item>
      <el-form-item label="纬度">
        <el-input v-model="form.lat"></el-input>
      </el-form-item>
      <el-form-item label="采样时间">
        <el-col :span="11">
          <el-date-picker
            v-model="form.date1"
            type="date"
            placeholder="Pick a date"
            style="width: 100%"
          />
        </el-col>
        <el-col :span="2" class="text-center">
          <span class="text-gray-500">-</span>
        </el-col>
        <el-col :span="11">
          <el-time-picker
            v-model="form.date2"
            placeholder="Pick a time"
            style="width: 100%"
          />
        </el-col>
      </el-form-item>
      
      <el-form-item label="海水温度">
        <el-input v-model="form.temp" ></el-input>
      </el-form-item>
      <el-form-item label="海平面高度">
        <el-input v-model="form.sl"></el-input>
      </el-form-item>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showDialog = false">Cancel</el-button>
        <el-button type="primary"  native-type="submit">Submit</el-button>
      </span>
    </el-form>
    
  </el-dialog>

  <el-dialog v-model="editVisible" title="编辑信息"  style="width:500px; z-index:100">
    <el-form :model="form_edit"  label-width="auto"  @submit.prevent="saveEdit">
      <el-form-item label="经度">
        <el-input v-model="form_edit.lon"></el-input>
      </el-form-item>
      <el-form-item label="纬度">
        <el-input v-model="form_edit.lat"></el-input>
      </el-form-item>
      <el-form-item label="采样时间">
        <el-input v-model="form_edit.date"></el-input>
      </el-form-item>
      
      <el-form-item label="海水温度">
        <el-input v-model="form_edit.temp" ></el-input>
      </el-form-item>
      <el-form-item label="海平面高度">
        <el-input v-model="form_edit.sl"></el-input>
      </el-form-item>
      <!-- Other form items -->

      <el-form-item>
        <el-button type="primary" native-type="submit">保存</el-button>
        <el-button @click="editVisible = false">取消</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>

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
  
  console.log(searchQuery.value);
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
  const userId = store.state.user_id;
  var username='';
  const showDialog = ref(false);
  const form = reactive({
    // pos: '',
    lon: '',
    lat: '',
    date1: '',
    date2: '',
    temp: '',
    sl: '',
    user_id: userId,
  });
  const form_edit=ref({
    // id: '',
    // lon: '',
    // lat: '',
    // date1: '',
    // date2: '',
    // temp: '',
    // sl: '',
    // user_id: userId,
  });
  const editVisible = ref(false);
  const selectedColumn = ref('');
  console.log('selectedColumn');
  console.log(selectedColumn.value);
  const columns = [
  {
    value: 'id',
    label: 'id',
  },
  {
    value: 'pos',
    label: '采样点',
  },
  {
    value: 'lon',
    label: '经度',
  },
  {
    value: 'lat',
    label: '纬度',
  },
  {
    value: 'time',
    label: '采样时间',
  },
  {
    value: 'temp',
    label: '海水温度',
  },
  {
    value: 'sl',
    label: '海平面高度',
  },
  
  {
    value: 'user_id',
    label: '录入人员',
  },
];
  
  //===函数定义======================================================
  const fetchData = async () => {
    const response = await axios.get(`/get_table`);
    tableData.value = response.data.dataList;
    console.log(tableData.value);
  };

  const getUserName = async () => {
      const response = await axios.get(`/get_user/${userId}`);
      const result = response.data;
      // 解构出各个属性数组
      username=result.username;
      // useradd.value=result.add;
      // userpassword.value=result.password;
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

  const handleEdit = (index, row) => {
    console.log(index, row);
    form_edit.value = { ...row };
    editVisible.value = true;
  }

  const saveEdit = async () => {
    try {
      console.log('form_edit');
      console.log(form_edit.value.id);
      const response = await axios.post(`/edit_save`, 
      {
        id: form_edit.value.id,
        lon: form_edit.value.lon,
        lat: form_edit.value.lat,
        date: form_edit.value.date,
        temp: form_edit.value.temp,
        sl: form_edit.value.sl,
        current_user: userId
      },
      {
          headers: {
              'Content-Type': 'application/json'
          }
      });
      tableData.value[form_edit.value.id-1] = {
        id: form_edit.value.id,
        pos:response.data.pos,
        lon: form_edit.value.lon,
        lat: form_edit.value.lat,
        date: form_edit.value.date,
        temp: form_edit.value.temp,
        sl: form_edit.value.sl,
        user_id: username,
      };
      console.log(response);
      editVisible.value = false;
      form_edit.value = {};
    } catch (error) {
      console.error('Error editing data:', error);
    }
  }

  const handleDelete = async (index, row) => {
    try {
      // Send a DELETE request to the backend
      console.log(index, row);
      //把row转换为json格式
      const row_json = JSON.stringify(toRaw(row));
      console.log(row_json);
      // console.log(tableData.value[index]);
      const response = await axios.post(`/delete_info`, row_json, {headers: {
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
    getUserName();
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
::v-deep .el-table--fit {
    border-bottom: 0;
    border-right: 0;
    margin-left: -10px !important;
}
</style>
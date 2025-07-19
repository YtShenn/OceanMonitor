<template>
    <div>
        <div class="container-scroller">
            <div class="container-fluid page-body-wrapper full-page-wrapper">
            <div class="content-wrapper d-flex align-items-center auth px-0">
                <div class="row w-100 mx-0">
                <div class="col-lg-4 mx-auto">
                    <div class="auth-form-light text-left py-5 px-4 px-sm-5">
                    <!-- <div class="brand-logo">
                        <img src="../../images/logo.svg" alt="logo">
                    </div> -->
                    <h4>Hello! let's get started</h4>
                    <h6 class="font-weight-light">Sign in to continue.</h6>
                    <form @submit.prevent="handleLogin" method="POST" class="pt-3">
                        <div class="form-group">
                        <!-- <input type="email" class="form-control form-control-lg" id="exampleInputEmail1" name="username" placeholder="Username"> -->
                        <input type="text" class="form-control form-control-lg" v-model="username" id="username" placeholder="Username">
                        </div>
                        <div class="form-group">
                        <input type="password" class="form-control form-control-lg" v-model="password" id="password" placeholder="Password">
                        </div>
                        <div class="mt-3">
                            <!-- <input type="submit" value="SIGN IN"><br><br> -->
                        <input class="btn btn-block btn-primary btn-lg font-weight-medium auth-form-btn" type="submit" value="SIGN IN"><br><br>
                        <!-- <a class="btn btn-block btn-primary btn-lg font-weight-medium auth-form-btn" href="../templates/manager.html">SIGN IN</a> -->
                        </div>
                        <div class="text-center mt-4 font-weight-light">
                        Don't have an account? <a href="register" class="text-primary">Create</a>
                        </div>
                    </form>
                    </div>
                </div>
                </div>
            </div>
            <!-- content-wrapper ends -->
            <div class="overlay"></div>
            </div>
            <!-- page-body-wrapper ends -->
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import qs from 'qs';
import {mapActions } from 'vuex';
import store from "../store/index";
import { ElMessage } from 'element-plus';

export default {
  data() {
    return {
      username: '',
      password: ''
    //   userType: 0 // Default user type is user
    };
  },
  methods: {
    ...mapActions(['login']),
    handleLogin() {
        let postData = qs.stringify({
            username: this.username,
            password: this.password
        })
        axios.post(`/login`, postData,
        {
            headers: {'Content-Type':'application/x-www-form-urlencoded'}
        }
        ).then(res => {
            console.log("login");
            console.log(res.status);
            console.log(res.data.status);
            console.log(res.data.user_id);
            console.log(res.data.user_type);
            if (res.status == 200 && res.data.status == "success") {
                this.login({user_id: res.data.user_id,isAdmin:res.data.user_type});
                console.log("登录成功");
                store.commit("setCurUserID",res.data.user_id);
                store.commit("setAdminState",res.data.user_type);
                localStorage.setItem("user",res.data.user_id);
                localStorage.setItem('is_admin', res.data.user_type);
                ElMessage.success({
                    message: "登录成功",
                    duration: 1500
                 });
                if(res.data.user_type == 1){
                  this.$router.push("/mainpage");
                }
                else{
                    this.$router.push("/userpage");
                }
            }
            else if (res.data.status === 'error') {
                this.$message.error("登录失败");
                console.log("登录失败");
                return;
            }
        })
        .catch(error => {
          if (error.response)
          {
            if (error.response.status === 401) {
              ElMessage.error({
                message: "用户名或密码错误",
                duration: 1500
              });
            }
            else {
              ElMessage.error({
                message: "登录失败：未知错误",
                duration: 1500
              });
            }
          }
          else {
            ElMessage.error({
              message: error,
              duration: 1500
            });
          }
        });
    },
  }
};

</script>
<style scoped>
    /* @import './src/assets/materialdesignicons.min.css'; */
</style>

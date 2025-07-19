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
                    <h4>New here?</h4>
                    <h6 class="font-weight-light">Signing up is easy. It only takes a few steps</h6>
                    <form method="POST" class="pt-3" @submit.prevent="handleRegister">
                        <div class="form-group">
                            <input type="text" class="form-control form-control-lg" id="username" v-model="username" placeholder="Username" required>
                            <span style="font-size: small; color: #9a9797;">   不超过10个英文字母、符号或数字</span>
                        </div>
                        <div class="form-group">
                            <input type="email" class="form-control form-control-lg" id="email" v-model="email" placeholder="Email" required>
                            <span style="font-size: small; color: #9a9797;">请填写正确的邮箱地址</span>
                        </div>                
                        <div class="form-group">
                            <input type="password" class="form-control form-control-lg" id="password" v-model="password" placeholder="Password" required>
                            <span style="font-size: small; color: #9a9797;">6~20个英文字母、符号或数字</span>
                        </div>
                        <div class="form-group user-type">
                            <el-radio-group v-model="userType" class="ml-4" style="display: flex; justify-content: space-between;">
                                <el-radio value=0 size="large" >普通用户</el-radio>
                                <el-radio value=1 size="large" >管理员</el-radio>
                            </el-radio-group>
                            <!-- <input class="form-check-input" type="checkbox" value="" name="is_manager" id="apply_manager">
                            <label class="form-check-label" for="defaultCheck1" style="color: #525252;">
                            申请管理员权限
                            </label> -->
                        </div>
                        <div v-if="userType == 1" class="form-group">
                            <!-- <label for="inviteCode">Invite Code</label> -->
                            <input type="text" class="form-control form-control-lg" id="inviteCode"  placeholder="Validation key" v-model="inviteCode" required />
                            <span style="font-size: small; color: #9a9797;">   输入管理员邀请码</span>
                        </div>
                        <!-- <div class="form-group" id="key-group" style="display: none;">
                            <input type="text" class="form-control form-control-lg" id="exampleInputPassword1" name="vkey" placeholder="Validation key">
                        </div> -->
                        
                        <div class="mt-3">
                            <input class="btn btn-block btn-primary btn-lg font-weight-medium auth-form-btn" type="submit" value="SIGN UP" ><br><br>
                        <!-- <a class="btn btn-block btn-primary btn-lg font-weight-medium auth-form-btn" href="../../index.html">SIGN UP</a> -->
                        </div>
                        <div class="text-center mt-4 font-weight-light">
                        Already have an account? <a id='lin' href="login" class="text-primary">Login</a>
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
import { mapActions } from 'vuex';
import { ElMessage } from 'element-plus';

export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      userType: 0, // Default user type is normal
      inviteCode: ''
    };
  },
  methods: {
    ...mapActions(['login']),
    validatePassword(password) {
      const minLength = 6;
      const hasUpperCase = /[A-Z]/.test(password);
      const hasLowerCase = /[a-z]/.test(password);
      const hasNumber = /[0-9]/.test(password);

      return password.length >= minLength &&
        ((hasUpperCase && hasLowerCase) ||
         (hasUpperCase && hasNumber) ||
         (hasLowerCase && hasNumber));
    },

    handleRegister() {
      if (!this.validatePassword(this.password)) {
        console.log("call");
        ElMessage.error({
          message: "密码长度必须至少为6位，且包含大小写字母和数字中的至少两种",
          duration: 1500,
        });
        return;
      }
      
      let postData = qs.stringify({
          username: this.username,
          email: this.email,
          password: this.password,
          userType: this.userType,
          inviteCode: this.inviteCode
      })
      // this.showTips(this.user.username)
      axios.post(`/register`, postData,
          {
              headers: {'Content-Type':'application/x-www-form-urlencoded'}
          })
          .then(res => {
              console.log("register");
              console.log(res.status);
              if (res.status === 200 && res.data=="success") {
                ElMessage.success({
                  message: "注册成功",
                  duration: 1500
                });
                  this.$router.push("/login")
              } 
          })
          .catch(error => {
            if (error.response && error.response.status === 401) {
              ElMessage.error({
                message: "邀请码错误",
                duration: 1500
              });
            }
            else if (error.response.status === 400){
              ElMessage.error({
                message: "用户名已占用，请选择其他用户名",
                duration: 1500
              });
            }
            else {
              console.log(error.response.status)
              ElMessage.error({
                message: "注册失败",
                duration: 1500
              });
            }
          }
        );
      }
    }
};
</script>

<style scoped>
    input[type="radio"] {
        margin-right: 5px;
        transform: scale(0.5);
        display: flex; 
        justify-content: space-between;
    }
    .user-type {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 20px 0;
    }

    .radio-label {
    font-weight: bold;
    color: #333;
    font-size: 0.9em;
    }

</style>


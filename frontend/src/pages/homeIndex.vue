<template>
    <div>
    <!-- <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js" integrity="sha384-/mhDoLbDldZc3qpsJHpLogda//BVZbgYuw6kof4u2FrCedxOtgRZDTHgHUhOCVim" crossorigin="anonymous"></script> -->
     <!-- 导航栏 -->
    <nav>
        <ul>
            <li><a href="#">Home</a></li>
            <li><a href="#">About</a></li>
            <li><a href="#">Contact</a></li>
            <li style="float: right;"><a href="#"><i class="bi bi-person-circle"></i></a></li>
            <li style="float: right;"> <a href="#">  未登录</a></li>

        </ul>
    </nav>

    <video autoplay muted loop id="myVideo" class="bg">
        <source src="../assets/waves.mp4" type="video/mp4">
    </video>
    <div class="overlay"></div>

    <!-- 标题 -->
    <div class="content">
        <div class="title">
            <h1>智慧海洋环境监测与分析系统</h1>
        </div>
        <!-- 按钮区域 -->
        <div class="button-area">
            
            <div class="button" onclick="location.href='login'">
                <i class="bi bi-person-fill-gear"></i>
                <span class="text">管理员 入口</span>
            </div>
            <div class="button" onclick="location.href='login'">
                <i class="bi bi-person-fill"></i>
                <span class="text">普通用户入口</span>
            </div>
        </div>
    </div>

    </div>
</template>

<script>
// export default {
//   name: 'Index',
// }
</script>

<style scoped>
    body {
        height: 100%;
        margin: 0;
        padding: 0;
        font-family: Arial, sans-serif;
    }
    html {
        height: 100%;
        margin: 0;
        font-family: Arial;
    }
    /* 设置导航栏样式 */
    nav {
        background-color: rgba(87, 91, 102, 0.7);
        color: rgb(65, 77, 93);
        padding: 10px 20px;
    }
    nav ul {
        list-style-type: none;
        margin: 0;
        padding: 0;
    }
    nav ul li {
        display: inline;
        margin-right: 20px;
    }
    nav ul li a,.bi.bi-person-circle{
        color:rgb(255, 255, 255);
        text-decoration: none;
        line-height: 1.5; 
        vertical-align: middle;
    }
    .bi.bi-person-circle{
        font-size: 20px;
        
        /* line-height: 1.5;  */
        /* padding-bottom: 15px; */
    }

    .bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
        z-index: -1; 
    }

    .overlay {
        position: fixed;
        top: 10;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgb(180, 198, 241);
        opacity: 0.25;
        z-index: 1;
    }

    .content {
        position: relative;
        z-index: 1;
        text-align: center;
        padding-top: 10%;
    }
    /* 设置标题样式 */
    .title {
        text-align: center;
        margin-top: 30px;
        font-size: 100px;
        color: #ffffff;
        padding: 25px 10px 20px 20px; /* 设置上下内边距为10px，左右内边距为20px，从而调整高度 */
        width: 40%; /* 设置宽度为父元素宽度的50%，从而调整宽度 */
        display: inline-block; 
        background-color: rgba(80, 80, 80, 0.7);
        border-radius: 15px;
    }

    .button-area {
        display: flex;
        justify-content: center;
        margin-top: 70px;
    }
    .button {
        border-radius: 15px;
        background-color:rgba(255, 255, 255, 0.7); /* 修改这一行 */
        width: 250px;
        height: 200px;
        margin: 30px 200px;
        /* border: 2px solid #333; */
        text-align: center;
        /* line-height: 150px; */
        font-size: 30px;
        cursor: pointer;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        position: relative;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5); 
    }
    .button .bi{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        visibility: visible;
    }
    .button .text {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        visibility: hidden;
    }

    .button:hover .bi {
        visibility: hidden;
    }

    .button:hover .text {
        visibility: visible;
    }
    .button:hover {
        background-color: rgba(172, 174, 174, 0.7); /* 修改这一行 */
        color: rgb(255, 255, 255);
    }
    .bi {
        font-size: 100px; /* 设置图标的大小 */
        color:#676767
    }
</style>
<template>
	<section>
		<!--工具条-->
		<el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
			<el-form :inline="true" :model="filters">
				<el-form-item>
					<el-input v-model="filters.name" placeholder="用户姓名"></el-input>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" v-on:click="selectUser">查询</el-button>
					<el-button type="primary" v-on:click="adduserr">添加</el-button>
					
				</el-form-item>
			</el-form>
		</el-col>

		<!--列表-->
		<el-table :data="users" highlight-current-row v-loading="listLoading" @selection-change="selsChange" style="width: 100%;">
			<!-- <el-table-column type="selection" width="55">
			</el-table-column> 
			<el-table-column type="index" width="80" label="序号" sortable>
			</el-table-column>-->
			<el-table-column prop="id" label="用户ID" width="180">
			</el-table-column>
			<el-table-column prop="name" label="用户姓名" width="180">
			</el-table-column>
			<el-table-column prop="role" label="用户角色" width="180">
			</el-table-column>
			<el-table-column prop="permission" label="用户权限" width="180">
			</el-table-column>
			<el-table-column prop="email" label="用户邮箱" width="180">
			</el-table-column>
			<el-table-column prop="date_joined" label="创建时间" width="480">
			</el-table-column>
			<!--<el-table-column prop="id" label="工号" width="150" sortable>
			</el-table-column>
			<el-table-column prop="email" label="邮箱" min-width="100" sortable>
			</el-table-column>90
			<el-table-column prop="superuser" label="类型" width="120" :formatter="formatSuperuser" sortable>
			</el-table-column>
			<el-table-column prop="permission" label="管理权限" width="120" :formatter="formatPermission" sortable>
			</el-table-column>-->
			<el-table-column label="操作" width="200">
				<template slot-scope="scope">
					<el-button size="small" @click="handleEdit(scope.$index, scope.row)">修改信息</el-button>
					<el-button size="small" @click="deleteEdit(scope.$index, scope.row)">删除</el-button>
				</template>
			</el-table-column>
			<!-- <el-table-column label="操作" width="300">
				<template slot-scope="scope">
					<el-button size="small" @click="adduserr()">新增用户</el-button>
				</template>
			</el-table-column> -->
		</el-table>

		<!--工具条-->
		<el-col :span="24" class="toolbar">
			<el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="20" :total="total" style="float:right;">
			</el-pagination>
		</el-col>

		<!-- 编辑界面 -->
		<el-dialog title="修改信息" v-model="editFormVisible" :close-on-click-modal="false">
			<el-form :model="editForm" label-width="120px" :rules="formRules" ref="editForm">
				
				<el-form-item label="员工账号" prop="name">
					<el-input v-model="editForm.name" :disabled="false"> </el-input>
				</el-form-item>
				<el-form-item label="邮箱" prop="email">
					<el-input v-model="editForm.email" :disabled="false" > </el-input>
				</el-form-item>
				<el-form-item label="权限" prop="permission">
					<el-select v-model="editForm.permission" name = "permission" placeholder="请选择权限">
						<el-option label="all" value="1"></el-option>
						<el-option label="select" value="2"></el-option>
						<el-option label="wed" value="3"></el-option>
					</el-select>
				</el-form-item>
				<el-form-item label="备注" prop="desc">
					<el-input type="textarea" v-model="editForm.desc"></el-input>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click.native="editFormVisible = false">取消</el-button>
				<el-button type="primary" @click.native="editSubmit" :loading="editLoading">提交</el-button>
				<!--<el-button size="small" @click="showChange()" style="float:left">密码重置</el-button>-->
				<el-button size="small" @click="deleteEdit()" style="float:left">删除</el-button>
			</div>
		</el-dialog> 

		<el-dialog title="密码重置" v-model="passwordFormVisible" :close-on-click-modal="false">
			<el-form :model="passwordForm" label-width="120px" :rules="passwordFormRules" ref="passwordForm">
				<el-form-item label="新密码" prop="password">
					<el-input v-model="passwordForm.password" :disabled="false"> </el-input>
				</el-form-item>
				<el-form-item label="再次输入密码" prop="password2">
					<el-input v-model="passwordForm.password2" :disabled="false"> </el-input>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click.native="passwordFormVisible = false">取消</el-button>
				<el-button type="primary" @click.native="changePassword" :loading="editLoading">提交</el-button>
			</div>
		</el-dialog>
	</section>
</template>

<script>
	import util from '../../common/js/util'
	import { getUserListPage, removeUser, batchRemoveUser, editUser, addUser } from '../../api/api';
	import Axios from 'axios';
	import { debug } from 'util';
	import { userInfo } from 'os';
	import { truncate } from 'fs';

	export default {
		data() {
			// 校验email
			var validateEmail = (rule, value, callback) =>{
				var reg = new RegExp("^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$");
				if (!value) {
					return callback(new Error('邮箱不能为空'));
				}else if(!reg.test(value)){
					return callback(new Error('邮箱格式错误'));
				}else{
					callback();
				}
			};
			// 校验密码
			var validatePassword = (rule, value, callback) =>{
				if (value === '') {
					return callback(new Error('请再次输入密码'));
				} else if (value !== this.passwordForm.password2) {
					return callback(new Error('两次输入密码不一致!'));
				} else {
					callback();
				}
			}
			return {
				filters: {
					name: ''
				},
				users: [],
				total: 0,
				page: 1,
				listLoading: false,
				sels: [],//列表选中列

				//修改信息界面数据
				editFormVisible: false,
				editLoading: false,
				editForm: {
					account: '',
					name: '',
					id: '',
					email: '',
					superuser: '',
					permission: 0,
					desc:''
				},
				formRules: {
					name: [
						{ required: true, message: '请输入账号', trigger: 'blur' },
						{ min: 5, max: 20, message: '长度在 5 到 20 个字符', trigger: 'blur' }
					],
					account: [
						{ required: true, message: '请输入客服姓名', trigger: 'blur' }
					],
					id: [
						{ required: true, message: '请输入客服工号', trigger: 'blur' }
					],
					email: [
						{  required: true , message: '请输入客服邮箱', trigger: 'blur' },
						{  validator: validateEmail, trigger: 'blur' }
					],
					permission: [
						{ required: true, message: '请输入客服权限', trigger: 'blur' }
					]
				},

				//修改密码界面数据
				passwordFormVisible : false,
				passwordForm:{
					password:'',
					password2:''
				},
				passwordFormRules:{
					password:[
						{ required: true, message: '请输入密码', trigger: 'blur' },
						{ min: 8, max: 20, message: '长度在 8 到 20 个字符', trigger: 'blur' }
					],
					password2:[
						{ required: true, message: '请输入密码', trigger: 'blur' },
						{ min: 8, max: 20, message: '长度在 8 到 20 个字符', trigger: 'blur' },
						{ validator:validatePassword}
					],
				}
			}
		},
		methods: {
			// 性别显示转换
			formatSuperuser: function (row, column) {
				return row.superuser == 1 ? '超级管理员' : row.superuser == 0 ? '客服' : '';
			},
			formatGuest: function (row, column) {
				return row.guest == 0 ? '注册登录' : row.guest == 1 ? '游客登录' : '未知';
			},
			formatPermission: function(row, column) {
				return row.permission == 1 ? '一级权限' : row.permission == 2 ? '二级权限' : row.permission == 3 ? '顶级权限' :'未知';
			},
			handleCurrentChange(val) {
				this.page = val;
				this.getUsers();
			},
			selectUser(val) {
				this.page = 1;
				this.getUsers();
			},
			//获取用户列表
			getUsers() {
				let para = {
					page: this.page,
					name: this.filters.name
				};
				
				this.listLoading = true;
				let token = sessionStorage.token || localStorage.token 
				if(this.filters.name){
					var url = "showuser/"+this.filters.name+'/'+ this.page +"/"
				}else{
					var url = "showuser/all/"+ this.page +"/"
				}
				
				this.$http.get(url, {
					headers: {
						'Authorization': 'JWT '+ token
					},
						responseType: 'json',
						withCredentials: true,
						page: this.page,
					})
					.then(response => {
						this.users = []
						console.log(response.data)
						if (response.data.data instanceof Array){
							console.log(response.data.list)
							
							for (let i of response.data.data){
								
								if(i.is_deleted==false){
									if(i.is_superuser==false){
										for (let item of response.data.list){
									console.log(i.is_superuser)
									
										if (item.username==i.username){
										this.users.push({
										"name":i.username,
										"id":i.id,
										'role':item['title'],
										'permission':item.feature,
										'email':i.email,
										'date_joined':i.date_joined

								
								})
									
									}}
									}
									else{
										this.users.push({
										"name":i.username,
										"id":i.id,
										'email':i.email,
										'role':'superuser',
										'permission':'all'
								
								})
									}
									
									
							
									
							}
								
							
							
						}
						}else{
							console.log(response.data.permission)
							permission = response.data.permission
							var permission = permission.join('-');
							console.log(permission)
							this.users.push({
								'name':response.data.username,
								'id' :response.data.id,
								'email':response.data.email,
								'role':response.data.title,
								'permission':permission,
								'date_joined':response.data.date_joined
							})
						}
						
						this.total = response.data.total;
						console.log(this.total)
						this.listLoading = false;
					})
					.catch(error => {
						console.log(error)
					})
			},
			adduserr:function(){

				this.$router.push({ path: '/adduser' })
			},
			
			
			//显示编辑界面
			handleEdit: function (index, row) {
				this.listLoading = true;
				// this.editForm = Object.assign({}, row);
				this.editForm = {}
				let token = sessionStorage.token || localStorage.token 
				var url = "/users/"+ row.id + "/"+ this.page +"/"
				
				this.$http.get(url,{
					headers: {
						'Authorization': 'JWT '+ token
					},
					responseType: 'json',
					withCredentials: true,
				})
				.then(response => {
					this.listLoading = false;
					let superuser = ""
					let user_info = response.data
					console.log(user_info)
					this.editForm = {
						user_id : user_info.id,
						account : user_info.user_name,
						name : user_info.username,
						id : user_info.work_id,
						email : user_info.email,
						superuser : superuser,
						permission : "",
						desc : user_info.desc
					}
					this.listLoading = false;
					this.editFormVisible = true;
				})
				.catch(error =>{
					if (error.response.status == 400){
						this.$message({
							message: error.response.data.message,
							type: 'error'
						});
						this.listLoading = false;
					}
					if (error.response.status == 500){
						this.$message({
							message: "服务器出错，请联系管理员",
							type: 'error'
						});
						this.listLoading = false;
					}
				})
			},
			set_out: function (index, row) {
				this.listLoading = true;
				let token = sessionStorage.token || localStorage.token 
				var url = "out/" + row.id + "/"
				this.$http.get(url, {
					headers: {
						'Authorization': 'JWT '+ token
					},
					responseType: 'json',
					withCredentials: true,
					})
					.then(response => {
						this.$message({
							message: '删除成功',
							type: 'success'
						});
						this.listLoading = false;
					})
			},
			//提交修改客服信息
			editSubmit: function () {
				// 判断信息缺失
				if (this.editForm.account == "" || this.editForm.name == "" || this.editForm.id == "" || this.editForm.permission == ""){
					this.$confirm('您提交的信息缺失，请补充信息！', '提示', {})
					return
				}
				this.$refs.editForm.validate((valid) => {
					if (valid) {
						this.$confirm('确认提交吗？', '提示', {}).then(() => {
							this.editLoading = true;
							let para = {
								"user_name" : this.editForm.account,
								"username": this.editForm.name,
								"id": this.editForm.id,
								"email": this.editForm.email,
								"is_superuser":this.editForm.superuser,
								"user_permission":this.editForm.permission,
								"desc":this.editForm.desc,
								"date1":1
							}
							
							let token = sessionStorage.token || localStorage.token;
							para.date_joined = util.formatDate.format(new Date(), 'yyyy-MM-dd hh:mm:ss');
							let url = "/users/"+ this.editForm.user_id + "/"
							this.$http.post(url,para, {
								headers: {
									'Authorization': 'JWT '+ token
								},
								responseType: 'json',
								withCredentials: true,
								}).then((res) => {
								this.editLoading = false;
								this.$message({
									message: '提交成功',
									type: 'success'
								})
								this.$refs['editForm'].resetFields();
								this.editFormVisible = false;
								this.getUsers();
							});
						});
					}
				});
			},

			selsChange: function (sels) {
				this.sels = sels;
			},
			// 密码重置窗口弹出
			showChange: function (){
				this.editFormVisible = false;
				this.passwordFormVisible = true
			},
			changePassword: function (index, row) {
				this.listLoading = true;
				let token = sessionStorage.token || localStorage.token 
				let para = {
					'password':this.passwordForm.password,
					'password2':this.passwordForm.password2
				}
				var url = "/changepassword/"+ this.editForm.user_id + "/"
				this.$refs.passwordForm.validate((valid) => {
					if (valid) {
						this.$http.put(url, para,{
							headers: {
								'Authorization': 'JWT '+ token
							},
							responseType: 'json',
							withCredentials: true,
						}).then(response =>{
							this.listLoading = false;
							this.passwordFormVisible = false;
							this.passwordForm = {}
						})
					}else{
						this.listLoading = false;
					}
				})
			},
			deleteEdit: function () {
				this.editFormVisible = false;
				this.$confirm('确认删除该名管理员的所有信息吗？', '提示', {}).then(()=>{
					this.listLoading = true;
					let token = sessionStorage.token || localStorage.token 
					var url = "/users/"+ this.editForm.user_id +'/'
					let para = {
						'is_deleted':1,
						'username' : this.editForm.name
					}
					console.log(para)
					this.$http.post(url, para,{
							
							headers: {
								'Authorization': 'JWT '+ token
							},
							responseType: 'json',
							withCredentials: true,
						}).then(response =>{
							console.log(para)
							this.listLoading = false;
							this.getUsers();
						})
					})		
			},

		},
		mounted() {
			console.log("begin")
			this.getUsers();
		}
	}

</script>

<style scoped>

</style>
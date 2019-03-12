<template>
	<el-form ref="form" :model="form" :rules="formRules" label-width="100px" @submit.prevent="onSubmit" style="margin:20px;width:80%;min-width:600px;">
		<el-form-item label="用户名" prop="username">
			<el-input v-model="form.username"></el-input>
		</el-form-item>
        <el-form-item label="密码" prop="password">
			<el-input type="password" v-model="form.password"></el-input>
		</el-form-item>
        <el-form-item label="再次输入密码" prop="password2">
			<el-input type="password" v-model="form.password2"></el-input>
		</el-form-item>
       
		<el-form-item label="邮箱" prop="email">
			<el-input v-model="form.email"></el-input>
		</el-form-item>
		<el-form-item label="用户角色" prop="value">
			<el-select v-model="value" multiple>
    			<el-option v-for="item in options5"  :key="item.value" :label="item.label" :value="item.value"></el-option>
  			</el-select>
		</el-form-item>
		<el-form-item label="备注" prop="desc">
			<el-input type="textarea" v-model="form.desc"></el-input>
		</el-form-item>
		<el-form-item>
			<el-button @click.native="addUser" type="primary">立即创建</el-button>
			<el-button @click.native.prevent='handleReset2'>重置</el-button>
		</el-form-item>
	</el-form>
</template>

<script>
	import util from '../../common/js/util'
	export default {
		data() {
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
			var validatePassword = (rule, value, callback) =>{

				if (value === '') {
				callback(new Error('请再次输入密码'));
				} else if (value !== this.form.password2) {
				callback(new Error('两次输入密码不一致!'));
				} else {
				callback();
				}
			}
			return {
				options5: [{
						value: '1',
						label: 'manager'
					}, {
						value: '2',
						label: 'staff'
					}, {
						value: '3',
						label: 'JavaScript'
        		}],
				value:[],
				
				// label:[],
				
				
			
			
				
				form: {
					username: '',
					password: '',
					password2: '',
					work_id: '',
					user_name: "",				
                    date_joined: '',
					value:[],
					desc: '',
					email:''
				},
				
				formRules: {
					username: [
						{ required: true, message: '请输入账号', trigger: 'blur' },
						{ min: 5, max: 20, message: '长度在 5 到 20 个字符', trigger: 'blur' }
					],
					password:[
						{ required: true, message: '请输入密码', trigger: 'blur' },
						{ min: 8, max: 20, message: '长度在 8 到 20 个字符', trigger: 'blur' }
					],
					password2:[
						{ required: true, message: '请输入密码', trigger: 'blur' },
						{ min: 8, max: 20, message: '长度在 8 到 20 个字符', trigger: 'blur' },
						{ validator:validatePassword}
					],
					user_name: [
						{ required: true, message: '请输入员工账号', trigger: 'blur' }
					],
					work_id: [
						{ required: true, message: '请输入客服工号', trigger: 'blur' }
					],
					email: [
						{  required: true , message: '请输入邮箱', trigger: 'blur' },
						{  validator: validateEmail, trigger: 'blur' }
					],
					// permission: [
					// 	{ required: true, message: '请输入角色', trigger: 'blur' },
					// ],
					// value: [
                	// 	{ required: true, message: '请输入角色', trigger: 'blur' },
					// ]
				},
			}
		},
		methods: {
            addUser () {
                let token = sessionStorage.token || localStorage.token
				let url = "homes/" 
				this.form.date_joined = util.formatDate.format(new Date(), 'yyyy-MM-dd hh:mm:ss');
				if (this.form.password != this.form.password2){
					this.$message({
						message: '两次输入密码不一致，请从新输入',
						type: 'error'
					});
					return
				};
				this.$refs.form.validate((valid) => {
					if (valid) {
						this.form['role'] = this.value
						console.log(this.form)
						this.$http.post( url,this.form,{                     
							headers: {
								'Authorization': 'JWT ' + token
							},
							contentType:"Content-Type",
							responseType: 'json',
							withCredentials: true
						}).then(response =>{
							this.$message({
								message: '添加成功',
								type: 'success'
							});
							location.reload();
						}).catch(error => {
							if (error.response.status == 400){
								this.$message({
									message: "信息错误或不完整，请检查信息",
									type: 'error'
								});
							}else if (error.response.status == 404){
								this.$router.push({ path: '/404' });
							}else if (error.response.status == 402){
								this.$message({
									message: error.response.data.message,
									type: 'error'
								});
							}
						})
					}
				})	
            },
			onSubmit() {
				console.log('submit!');
			},
			handleReset2() {
				location.reload();
			},
		}
	}

</script>
<template>
	<el-form ref="form" :model="form" :rules="formRules" label-width="100px" @submit.prevent="onSubmit" style="margin:20px;width:80%;min-width:600px;">
		<el-form-item label="权限名" prop="permissionname">
			<el-input v-model="form.feature"></el-input>
		</el-form-item>
		<el-form-item label="url名" prop="urlname">
			<el-input v-model="form.url"></el-input>
		</el-form-item>
			<el-button @click.native="addpermission" type="primary">立即创建</el-button>
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
				
				form: {
					feature: '',
					url:'',
					
				},
				
				// formRules: {
				// 	permissionname: [
				// 		{ required: true, message: '请输入权限', trigger: 'blur' },
						// { min: 1, max: 20, message: '长度在 5 到 20 个字符', trigger: 'blur' }
					// ],
					
					// urlname: [
						// { required: true, message: '请输入url', trigger: 'blur' },
					// ],
					// value: [
                	// 	{ required: true, message: '请输入角色', trigger: 'blur' },
					// ]
				// },
			}
		},
		methods: {
            addpermission () {
                let token = sessionStorage.token || localStorage.token
				let url = "addnewpermission/" 
				// this.form.date_joined = util.formatDate.format(new Date(), 'yyyy-MM-dd hh:mm:ss');
				this.$refs.form.validate((valid) => {
					if (valid) {
						console.log(this.form)
						// this.form['url'] = this
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
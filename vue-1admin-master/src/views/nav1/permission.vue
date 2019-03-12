<template>
	<el-form ref="form" :model="form" :rules="formRules" label-width="100px" @submit.prevent="onSubmit" style="margin:20px;width:80%;min-width:600px;">
		<el-form-item label="用户角色" prop="role">
			<el-select v-model="value" multiple>
    			<el-option v-for="item in options"  :key="item.value" :label="item.label" :value="item.value"></el-option>
  			</el-select>
		</el-form-item>
		<el-form-item label="用户权限" prop="permission">
			<el-select v-model="value1" multiple>
    			<el-option v-for="item in options1"  :key="item.value" :label="item.label" :value="item.value"></el-option>
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
			
			return {

				options1: [{
						value: '1',
						label: 'all'
					}, {
						value: '2',
						label: 'select'
					}, {
						value: '3',
						label: 'wed'
        		}],
				value1:[],
				options: [{
						value: 'Manage',
						label: 'Manage'
					}, {
						value: 'staff',
						label: 'staff'
					}, {
						value: 'JavaScript',
						label: 'JavaScript'
        		}],
				value:[],
				
				form: {
					
					// value:[],
					
				},
				
				formRules: {
				
					role: [
						{ required: true, message: '请输入角色', trigger: 'blur' },
					],
					permission: [
						{ required: true, message: '请输入权限', trigger: 'blur' },
					],
					
				},
			}
		},
		methods: {
            addUser () {
                let token = sessionStorage.token || localStorage.token
				let url = "addpermission/" 	
				this.form['permission'] = this.value1
				this.form['title'] =String(this.value)
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
		},	
	
			onSubmit() {
				console.log('submit!');
			},
			handleReset2() {
				location.reload();
			},
		}
	

</script>
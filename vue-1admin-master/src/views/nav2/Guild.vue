<template>
	<section>
		<!--工具条-->
		<el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
			<el-form :inline="true" :model="filters">
				<el-form-item>
					<el-input v-model="filters.id" placeholder="玩家ID"></el-input>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" v-on:click="selectUser">查询</el-button>
				</el-form-item>
			</el-form>
		</el-col>

		<!--列表-->
		<el-table :data="users" highlight-current-row v-loading="listLoading" @selection-change="selsChange" style="width: 100%;">
			<el-table-column type="index" width="80" label="序号" sortable>
			</el-table-column>
            <el-table-column prop="sm_playerid" width="80" label="ID" sortable>
			</el-table-column>
			<el-table-column prop="sm_playername" label="玩家名称" width="150">
			</el-table-column>
			<el-table-column prop="sm_guildid" label="公会ID" width="120" sortable>
			</el-table-column>
			<el-table-column prop="sm_guildname" label="公会名称" width="150" sortable>
			</el-table-column>
			<el-table-column prop="sm_type" label="类型" width="150" sortable>
			</el-table-column>
            <el-table-column prop="sm_action" label="操作" width="150" sortable>
			</el-table-column>
            <el-table-column prop="sm_contributegold" label="贡献金币" width="150" sortable>
			</el-table-column>
			<el-table-column prop="sm_toplayerid" label="目标玩家ID" min-width="150" sortable>
			</el-table-column>
            <el-table-column prop="sm_toplayername" label="目标玩家名称" min-width="150" sortable>
			</el-table-column>
            <el-table-column prop="sm_giftnum" label="礼物数量" width="150" sortable>
			</el-table-column>
            <el-table-column prop="sm_giftname" label="礼物名称" width="200" sortable>
			</el-table-column>
			<el-table-column prop="sm_logat" label="时间" width="200" sortable>
			</el-table-column>
		</el-table>

		<!--工具条-->
		<el-col :span="24" class="toolbar">
			<el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="20" :total="total" style="float:right;">
			</el-pagination>
		</el-col>
	</section>
</template>

<script>
	import util from '../../common/js/util'
	//import NProgress from 'nprogress'
	import { getUserListPage, removeUser, batchRemoveUser, editUser, addUser } from '../../api/api';
	import Axios from 'axios';
	import { debug } from 'util';

	export default {
		data() {
			return {
				filters: {
					id: ''
				},
				users: [],
				total: 0,
				page: 1,
				listLoading: false,
				sels: [],//列表选中列
			}
		},
		methods: {
			// 性别显示转换
			formatOutRoom: function (row, column) {
				return row.outroom == "" ? '未正常退出' : row.outroom;
			},
			formatGuest: function (row, column) {
				return row.guest == 0 ? '注册登录' : row.guest == 1 ? '游客登录' : '未知';
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
					id: this.filters.id
				};
				this.listLoading = true;
				let token = sessionStorage.token || localStorage.token 
				var url = "/log/guildlog/"+ this.filters.id + "/" + this.page + "/"
				console.log(url)
				this.$http.get(url, {
					headers: {
						'Authorization': 'JWT '+ token
					},
					responseType: 'json',
					withCredentials: true,
					page: this.page,
					id: this.filters.id
					})
					.then(response => {
                        this.users = []
						for (let i of response.data.data){
							this.users.push({
                                "sm_playerid":i.sm_playerid,
								"sm_playername":i.sm_playername,
								"sm_guildid":i.sm_guildid,
                                "sm_guildname":i.sm_guildname,
                                "sm_type":i.sm_type,
                                "sm_action":i.sm_action,
                                "sm_contributegold":i.sm_contributegold,
                                "sm_toplayerid":i.sm_toplayerid,
                                "sm_toplayername":i.sm_toplayername,
                                "sm_giftnum":i.sm_giftnum,
								"sm_gifttype":i.sm_gifttype,
								"sm_giftname":i.sm_giftname,
								"sm_logat":i.sm_logat,
								})
					}
					this.total = response.data.total;
					this.listLoading = false;
					})
					.catch(error => {
						if (error.response.status == 400){
							this.$message({
								message: error.response.data.message,
								type: 'error'
							});
							this.listLoading = false;
						}
					})
			},
			selsChange: function (sels) {
				this.sels = sels;
			},
		},
	}

</script>

<style scoped>

</style>
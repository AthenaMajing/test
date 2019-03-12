import Login from './views/Login.vue'
import NotFound from './views/404.vue'
import Home from './views/Home.vue'
import Main from './views/Main.vue'
import Table from './views/nav1/Table.vue'
import permission from './views/nav1/permission.vue'
// import Form from './views/nav1/Form.vue'
import roleshow from './views/nav1/roleshow.vue'
import Guild from './views/nav2/Guild.vue'
import Room from "./views/nav2/Room.vue"
import Prop from './views/nav2/Prop.vue'
import Add from './views/nav3/Add.vue'
import Show from './views/nav3/Show.vue'
import echarts from './views/charts/echarts.vue'
import updateinfor from './views/nav3/updateinfor.vue'

let routes = [
    {
        path:'/update',
        component:updateinfor,
        name:'',
        hidden:true
    },
    {
        path: '/login',
        component: Login,
        name: '',
        hidden: true
    },
    {
        path: '/404',
        component: NotFound,
        name: '',
        hidden: true
    },
    // { path: '/main', component: Main },
    {
        path: '/',
        component: Home,
        name: 'Charts',
        iconCls: 'fa fa-bar-chart',
        hidden: true,
        children: [
            { path: '/echarts', component: echarts, name: 'echarts' },
            // { path: '/update', component: updateinfor, name: '修改信息' }
        ]
    },
    {
        path: '/Permission',
        component: Home,
        name: '角色管理',
        iconCls: 'el-icon-message',//图标样式class,
        hidden: true,
        children: [
            { path: '/main', component: Main, name: '角色列表',hidden:true },
            { path: '/roleshow', component: roleshow, name: '角色列表' },
            { path: '/table', component: Table, name: '新增角色',hidden:true},
            { path: '/permission', component: permission, name: '权限分配',hidden:true},
           
            
        ]
    },
    {
        path: '/Rome',
        component: Home,
        name: '权限管理',
        iconCls: 'fa fa-id-card-o',
        hidden: true,
        children: [
            { path: '/rome', component: Room, name: '权限列表' },
            { path: '/prop', component: Prop, name: '新增权限',hidden:true },
            { path: '/guild', component: Guild, name: '分配权限',hidden:true }
        ]
    },
    {
        path: '/User',
        component: Home,
        name: '添加用户',
        iconCls: 'fa fa-address-card',
        hidden: true,
        // leaf: true,//只有一个节点
        children: [
            { path: '/showUser', component: Show, name: '用户列表' },
            { path: '/addUser', component: Add, name: '添加用户' ,hidden:true},
            { path: '/update', component: updateinfor, name: '修改信息',hidden:true}

        ]
    },

    {
        path: '*',
        hidden: true,
        redirect: { path: '/404' },
    

    },
   
];

export default routes;
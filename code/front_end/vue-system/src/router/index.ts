import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router';
import { usePermissStore } from '../store/permiss';
import Home from '../views/home.vue';

const routes: RouteRecordRaw[] = [
    {
        path: '/',
        //修改开始页面为首页
        //TODO 需要改为搜索界面
        redirect: '/dashboard',
    },
    {
        path: '/',
        name: 'Home',
        component: Home,
        children: [
            {
                path: '/dashboard',
                name: 'dashboard',
                meta: {
                    title: '系统首页',
                    permiss: '1',
                },
                component: () => import(/* webpackChunkName: "dashboard" */ '../views/dashboard.vue'),
            },
            
            {
                path: '/generate',
                name: 'generate',
                meta: {
                    title: '主页',
                    permiss: '1',
                },
                component: () => import(/* webpackChunkName: "Generate" */ '../views/Generate.vue'),
            },
            {
                path: '/Diarization',
                name: 'Diarization',
                meta: {
                    title: '可视化',
                    permiss: '1',
                },
                component: () => import(/* webpackChunkName: "Diarization" */ '../views/Diarization.vue'),
            },
            {
                path: '/GetUserCollections',
                name: 'GetUserCollections',
                meta: {
                    title: '收藏',
                    permiss: '2',
                },
                component: () => import(/* webpackChunkName: "Diarization" */ '../views/GetUserCollections.vue'),
            },
            {
                path: '/SearchEngine',
                name: 'SearchEngine',
                meta: {
                    title: '搜索',
                    permiss: '1',
                },
                component: () => import(/* webpackChunkName: "Search" */ '../views/SearchEngine.vue'),
            },
            {
                path: '/SearchResult',
                name: 'SearchResult',
                meta: {
                    title: '搜索结果',
                    permiss: '1',
                },
                component: () => import(/* webpackChunkName: "Search" */ '../views/SearchResult.vue'),
            },
            {
                path: '/permission',
                name: 'permission',
                meta: {
                    title: '权限管理',
                    permiss: '7',
                },
                component: () => import(/* webpackChunkName: "permission" */ '../views/permission.vue'),
            },
            {
                path: '/user',
                name: 'user',
                meta: {
                    title: '个人中心',
                },
                component: () => import(/* webpackChunkName: "user" */ '../views/user.vue'),
            },
            {
                path: '/visualization/author/:author_id',
                name: 'AuthorVisualization',
                meta: {
                    title: 'AuthorVisualization',
                    permiss: '1',
                },
                component: () => import(/* webpackChunkName: "import" */ '../views/AuthorVisualization.vue'),
            },
            {
                path: '/visualization/paper/:paper_id',
                name: 'PaperVisualization',
                meta: {
                    title: 'PaperVisualization',
                    permiss: '1',
                },
                component: () => import(/* webpackChunkName: "import" */ '../views/PaperVisualization.vue'),
            },
            {
                path: '/search/search_visualization',
                name: 'SearchResultVisualization',
                meta: {
                    title: 'SearchResultVisualization',
                    permiss: '1',
                },
                component: () => import(/* webpackChunkName: "import" */ '../views/SearchResultVisualization.vue'),
            },
            {
                path: '/information/authors/:author_id',
                name: 'AuthorPage',
                meta: {
                    title: 'AuthorPage',
                    permiss: '1',
                },
                component: () => import(/* webpackChunkName: "import" */ '../views/PageAuthor.vue'),
            },
            {
                path: '/information/papers/:paper_id',
                name: 'PaperPage',
                meta: {
                    title: 'PaperPage',
                    permiss: '1',
                },
                component: () => import(/* webpackChunkName: "import" */ '../views/PagePaper.vue'),
            },
        ],
    },
    {
        path: '/login',
        name: 'Login',
        meta: {
            title: '登录',
        },
        component: () => import(/* webpackChunkName: "login" */ '../views/login.vue'),
    },
    {
        path: '/register', // 添加注册页面的路由
        name: 'register',
        meta: {
            title: '注册',
        },
        component: () => import(/* webpackChunkName: "register" */ '../views/register.vue'),
    },

    {
        path: '/403',
        name: '403',
        meta: {
            title: '没有权限',
        },
        component: () => import(/* webpackChunkName: "403" */ '../views/403.vue'),
    },
];

const router = createRouter({
    history: createWebHashHistory(),
    routes,
});


router.beforeEach((to, from, next) => {
    document.title = `${to.meta.title} | vue-manage-system`;
    const role = localStorage.getItem('ms_username');
    const permiss = usePermissStore();
    // if (!role && to.path !== '/login') {
    //     next('/login');
    // } else if (to.meta.permiss && !permiss.key.includes(to.meta.permiss)) {
    //     // 如果没有权限，则进入403
    //     next('/403');
    // } 
    // else if(!role){
    //     next('/register');
    // }
    //else{
        next();
    //}
});

export default router;

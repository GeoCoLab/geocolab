<template>
  <nav class="p-4 w-full col-span-3 grid items-center relative" id="page-nav">
    <!-- logo -->
    <a href="/" id="nav-icon">
      <img :src="logo" class="w-10" alt="GeoCoLab">
    </a>
    <!-- menu button -->
    <vue-feather type="menu" v-if="!isLarge" @click="expandMenu = !expandMenu"
                 :aria-expanded="expandMenu" aria-controls="main-menu" />
    <!-- link block 1 -->
    <div id="nav-links">
      <Dropdown v-if="!isLarge" :show="expandMenu" id="main-menu" @toggle-dropdown="toggleMenu">
        <NavBlock :links="links" direction="col" />
      </Dropdown>
      <NavBlock v-else :links="links" direction="row"/>
    </div>
    <!-- end link block 1-->
    <!-- link block 2 -->
    <div id="nav-auth">
      <NavBlock direction="row">
        <template v-if="auth.loggedIn">
          <NavItem path="/user/account">
            <span class="<md:hidden">Hi, {{ auth.userData.given_name }}</span>
            <img :src="auth.userData.gravatar + '&s=30'" class="inline md:ml-4 rounded-full border-2 border-secondary-light">
          </NavItem>
          <NavItem path="#" label="Logout" @click="auth.logout">
          </NavItem>
        </template>
        <template v-else>
          <NavItem path="/user/login" label="Login" />
          <NavItem path="/user/register" label="Register" />
        </template>
      </NavBlock>
    </div>
    <!-- end link block 2 -->
  </nav>
</template>

<script setup>
import logo from '../assets/logo.png';
import NavBlock from './nav/NavBlock.vue';
import NavItem from './nav/NavItem.vue';
import { breakpointsTailwind, useBreakpoints } from '@vueuse/core';
import { computed, ref } from 'vue';
import Dropdown from './nav/Dropdown.vue';
import { useAuthStore } from '../store/auth';

const auth = useAuthStore();

const breakpoints = useBreakpoints(breakpointsTailwind);
const isLarge = ref(breakpoints.greater('lg'));

const expandMenu = ref(false);

const defaultRoutes = [
  {
    path: '/',
    label: 'Home'
  },
  {
    path: '/about',
    label: 'About',
    dropdown: [
      {
        path: '/about/coc',
        label: 'Code of Conduct'
      },
      {
        path: '/about/terms',
        label: 'Terms & Conditions'
      }
    ]
  },
  {
    path: '/blog',
    label: 'Blog'
  },
];
const hiddenRoutes = [
  {
    path: '/admin',
    label: 'Admin',
    access: ['admin']
  },
  {
    path: '/researcher',
    label: 'Researcher',
    access: ['researcher'],
    dropdown: [
      {
        path: '/applications',
        label: 'Applications',
        dropdown: [
          {
            path: '/applications/new',
            label: 'New'
          }
        ]
      }
    ]
  },
  {
    path: '/manager',
    label: 'Manager',
    access: ['manager'],
    dropdown: [
      {
        path: '/orgs',
        label: 'Organisations/Institutions',
        dropdown: [
          {
            path: '/orgs/new',
            label: 'New'
          }
        ]
      },
      {
        path: '/facilities',
        label: 'Facilities',
        dropdown: [
          {
            path: '/facilities/new',
            label: 'New'
          }
        ]
      },
      {
        path: '/review',
        label: 'Applications'
      }
    ]
  }
];

function canAccess(roles) {
  if (auth.userData.role === 'admin') {
    return true;
  } else {
    return roles.includes(auth.userData.role);
  }
}

const links = computed(() => {
  let allowedLinks = hiddenRoutes.filter(r => canAccess(r.access));
  return [...defaultRoutes, ...allowedLinks];
});

function toggleMenu(state) {
  expandMenu.value = state;
}

</script>

<style scoped>

</style>

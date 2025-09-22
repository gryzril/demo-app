<template>
  <div id="app">
    <!-- Navigation Links -->
    <nav>
      <ul>
        <li><router-link to="/">Dashboard</router-link></li>
        <li><router-link to="/login">Login</router-link></li>
      </ul>
    </nav>

    <!-- Render the current route's component -->
    <router-view></router-view>
  </div>
</template>

<script setup>
import { defineComponent } from 'vue';
import { useRouter } from 'vue-router';
</script>

<style>
nav {
  margin-bottom: 20px;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin-right: 10px;
}
</style>

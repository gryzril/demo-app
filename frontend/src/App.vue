<template>
  <nav>
    <ul>
      <li><router-link to="/">Dashboard</router-link></li>
      <li><router-link to="/login">Login</router-link></li>
    </ul>
  </nav>

  <RouterView v-slot="{ Component }">
    <component v-if="Component" :is="Component" />
  </RouterView>
</template>

<script setup>
</script>

<style>
nav { margin-bottom: 20px; }
ul { list-style: none; padding: 0; }
li { display: inline-block; margin-right: 10px; }
</style>

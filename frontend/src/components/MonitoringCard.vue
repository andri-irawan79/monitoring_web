<script setup>
defineProps({
  title: String,
  value: [String, Number]
})
</script>

<template>
  <div class="card">
    <h3>{{ title }}</h3>
    <p>{{ value }}</p>
  </div>
</template>

<style scoped>
.card{
  border:1px solid #ddd;
  border-radius:10px;
  padding:20px;
  text-align:center;
  background:white;
}

h3{
  margin:0;
}

p{
  font-size:24px;
  font-weight:bold;
}
</style>

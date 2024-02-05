<template>
  <router-view />
</template>

<script>

export default {
  name: "APP",
  components: {

  },
  resolve: {
      modules: ["src", "node_modules"],
  }
}
</script>

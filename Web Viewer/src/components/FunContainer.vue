<template>
  <div class="main-container">
    <router-view :variables="variables" :typefaceStyle="typefaceStyle"></router-view>
  </div>
</template>

<script>
export default {
  name: 'FunContainer',
  data() {
    return {
      currentTab: 'headline'
    }
  },
  computed: {
    typefaceStyle() {
      return this.$store.getters.typefaceStyle;
    },
    variables() {
      return this.$store.getters.variables;
    }
  }
}
</script>

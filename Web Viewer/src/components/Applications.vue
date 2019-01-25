<template>
  <div class="main-container">
    <md-tabs class="fixed-tabs" @md-changed="tabChanged">
      <md-tab id="news" md-label="News"></md-tab>
      <md-tab id="inbox" md-label="Inbox"></md-tab>
      <md-tab id="email" md-label="Email"></md-tab>
      <md-tab id="calendar" md-label="Calendar"></md-tab>
      <md-tab id="search" md-label="Search"></md-tab>
    </md-tabs>
    <div :style="typefaceStyle" class="google-text">
      <Calendar v-if="currentTab === 'calendar'" :variables="variables" />
      <Inbox v-if="currentTab === 'inbox'" :variables="variables" />
      <Email v-if="currentTab === 'email'" :variables="variables" />
      <News v-if="currentTab === 'news'" :variables="variables" />
      <Search v-if="currentTab === 'search'" :variables="variables" />
    </div>
  </div>
</template>

<script>
import Calendar from './applications/Calendar.vue';
import Inbox from './applications/Inbox.vue';
import Email from './applications/Email.vue';
import News from './applications/News.vue';
import Search from './applications/Search.vue';
export default {
  name: 'Applications',
  components: {
    Calendar,
    Inbox,
    Email,
    News,
    Search
  },
  props: ['variables', 'typefaceStyle'],
  data() {
    return {
      currentTab: 'news'
    }
  },
  methods: {
    tabChanged(id) {
      this.currentTab = id;
    }
  }
}
</script>

<style lang="scss" scoped>
  .fixed-tabs {
    position: fixed;
  }
</style>

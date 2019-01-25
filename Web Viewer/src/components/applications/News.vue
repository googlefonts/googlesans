<template>
  <div class="single-phone-center">
    <div :style="variables" class="mobile-phone md-elevation-8">
      <p class="news-your-briefing">Phillipe’s Briefing</p>
      <p class="news-top-5">Top 5 stories right now</p>
      <p class="news-temperature">25°C</p>
      <p class="news-headline-one">Five ways the government shutdown could end – and why they probably won’t happen</p>
      <p class="news-headline-info-one">Headlines – 1 hour ago</p>
      <p class="news-headline-two">China sentences Canadian man to death in drug case linked to Huawei row</p>
      <p class="news-headline-info-two">Headlines – 13 minutes ago</p>
      <img src="@/assets/images/8318516d017f5caadb2c73b55cbea5d33e6b7987-crop.png" alt="">
    </div>
  </div>
</template>

<script>
export default {
  name: 'News',
  props: ['variables']
}
</script>

<style lang="scss" scoped>
  .news-your-briefing {
    position: fixed;
    top: 12.5%;
    font-size: 1.75vh;
    text-align: left;
    padding-left: 1.2em;
    padding-right: 1.2em;
  }

  .news-top-5 {
    position: fixed;
    top: 16.25%;
    font-size: 1.25vh;
    text-align: left;
    padding-left: 1.75em;
    padding-right: 1.2em;
  }

  .news-temperature {
    position: fixed;
    top: 17.5%;
    left: 82%;
    font-size: 1vh;
    text-align: left;
    padding-left: 0.9em;
    padding-right: 0.9em;
  }

  .news-headline-one {
    position: fixed;
    top: 50%;
    font-size: 1.75vh;
    text-align: left;
    padding: 0.75em 1.5em 1.2em 2.2em;
  }

  .news-headline-info-one {
    position: fixed;
    top: 63.25%;
    font-size: 1.25vh;
    text-align: left;
    padding-left: 3.05em;
    padding-right: 1.2em;
  }

  .news-headline-two {
    position: fixed;
    top: 71.5%;
    font-size: 1.25vh;
    text-align: left;
    padding: 0.75em 10em 1.2em 3em;
  }

  .news-headline-info-two {
    position: fixed;
    top: 82.25%;
    font-size: 1.25vh;
    text-align: left;
    padding-left: 2.95em;
    padding-right: 1.2em;
  }

</style>

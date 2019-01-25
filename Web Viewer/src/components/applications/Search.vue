<template>

  <div class="single-phone-center">
    <div :style="variables" class="mobile-phone md-elevation-8">
      <p class="search-search-term">Transportation Security Administ...</p>
      <p class="search-title-one">Houston Airport shuts down TSA security checkpoint amid government shutdown | TheHill</p>
      <p class="search-subtitle-one">The Houston Bush Airport on Sunday closed the Transportation Security Administration (TSA) c...</p>
      <p class="search-time-one">The Hill – 14 hours ago</p>
      <p class="search-related">RELATED</p>
      <p class="search-related-one">Traveler carried firearm through TSA checkpoint at Atlnata airport | TheHill</p>
      <p class="search-related-time">The Hill – 13 hours ago</p>
      <!-- <p class="search-related-two">Traveler carried firearm through TSA checkpoint at Atlnata airport | TheHill</p> -->
      <!-- <p class="search-customise-discover">Customise Discover</p> -->
      <img src="@/assets/images/c0c8ae0a49f6e3e924a688230f3f55b5ecdcf633-crop.png" alt="">
    </div>
  </div>



</template>

<script>
export default {
  name: 'Search',
  props: ['variables']
}
</script>

<style lang="scss" scoped>
  .search-search-term {
    position: fixed;
    top: 2.8%;
    font-size: 1.25vh;
    text-align: left;
    padding: 0.75em 1.2em 1.2em 7.2em;
  }

  .search-title-one {
    position: fixed;
    top: 36.5%;
    font-size: 1.66vh;
    text-align: left;
    padding-left: 2em;
    padding-right: 2em;
  }

  .search-subtitle-one {
    position: fixed;
    top: 47.5%;
    font-size: 1.25vh;
    text-align: left;
    padding-left: 2.66em;
    padding-right: 1.2em;
  }

  .search-related {
    position: fixed;
    top: 61%;
    font-size: 1vh;
    text-align: left;
    padding: 0.75em 1.2em 1.2em 3.33em;
  }

  .search-related-one {
    position: fixed;
    top: 65%;
    font-size: 1vh;
    text-align: left;
    padding: 0.75em 18em 1.2em 3.33em;
  }

  .search-related-time {
    position: fixed;
    top: 72.75%;
    font-size: 1vh;
    text-align: left;
    padding: 0.75em 1.2em 1.2em 5.25em;
  }

  .search-time-one {
    position: fixed;
    top: 53.33%;
    font-size: 1vh;
    text-align: left;
    padding: 0.75em 1.2em 1.2em 5.25em;
  }
</style>

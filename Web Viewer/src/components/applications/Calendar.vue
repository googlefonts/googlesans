<template>
  <div class="single-phone-center">
    <div :style="variables" class="mobile-phone md-elevation-8">
      <p class="calendar-event-title">Component building very best practices</p>
      <p class="calendar-date-time">Monday, Jan 14・2–3 PM</p>
      <p class="calendar-event-information">
        NYC-9TH-14-E-Phone Room 14E322 (1) [GVC, No External Guests, Phone] <br>
        SFO-SPE-4-El Camino Del Mar (7) [GVC]
       </p>
       <p class="calendar-event-information-two">
         NYC-9TH-14-E-Phone Room 14E322 (1) [GVC, No External Guests, Phone] <br>
         SFO-SPE-4-El Camino Del Mar (7) [GVC]
        </p>
       <p class="calendar-join-call">
         <span class="join-us">Join video call</span> <br>
         meet.google.com/wsd-qanw-yro <br>
         <br>
         <span class="join-us">Join by phone</span> <br>
         (US) +1 443-671-4750 PIN: 647468
       </p>
       <p class="calendar-extra-info">
         More phone numbers
       </p>
       <p class="calendar-extra-info-reminder">
         10 minutes before
       </p>
      <img src="@/assets/images/4ccc4b90b375a05722a671b29b4d23811ca9a5a5-crop.png" alt="">
    </div>
  </div>
</template>

<script>
export default {
  name: 'Calendar',
  props: ['variables']
}
</script>

<style lang="scss" scoped>
  .calendar-event-title {
    position: fixed;
    top: 11.1%;
    font-size: 2vh;
    text-align: left;
    padding-left: 2.8em;
    padding-right: 2.8em;
  }

  .calendar-date-time {
    position: fixed;
    top: 19%;
    font-size: 1.5vh;
    text-align: left;
    padding-left: 3.75em;
    padding-right: 1.75em;
  }

  .calendar-event-information {
    position: fixed;
    top: 28%;
    font-size: 1.5vh;
    text-align: left;
    padding-left: 3.75em;
    padding-right: 1.75em;
  }

  .calendar-event-information-two {
    position: fixed;
    top: 43.5%;
    font-size: 1.5vh;
    text-align: left;
    padding-left: 3.75em;
    padding-right: 1.75em;
  }

  .calendar-join-call {
    position: fixed;
    top: 59.33%;
    font-size: 1.25vh;
    text-align: left;
    padding-left: 4.5em;
    padding-right: 1.75em;
  }

  .calendar-extra-info {
    position: fixed;
    top: 77.25%;
    font-size: 1.25vh;
    text-align: left;
    padding-left: 4.5em;
    padding-right: 1.75em;
  }

  .calendar-extra-info-reminder {
    position: fixed;
    top: 83.75%;
    font-size: 1.25vh;
    text-align: left;
    padding-left: 4.5em;
    padding-right: 1.75em;
  }

  .join-us {
    color: var(--md-theme-default-primary);
    font-size: 1.2em
  }
</style>

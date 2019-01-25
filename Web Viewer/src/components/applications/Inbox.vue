<template>
  <div class="single-phone-center" :style="variables">
    <div class="mobile-phone md-elevation-8">
      <p class="inbox-names-1">me</p>
      <p class="inbox-subject-1">Subject of an email with an attachment</p>
      <p class="inbox-time-1">10:23 AM</p>
      <p class="inbox-attachment-1">IMG_6399.jpg</p>

      <p class="inbox-names-2">connieshi, ricardocr</p>
      <p class="inbox-subject-2">An unread email subject line</p>
      <p class="inbox-time-2">10:29 AM</p>
      <p class="inbox-snippet-2">Snippet of the email content goes here...</p>

      <p class="inbox-names-3">Markus Schmeiduch</p>
      <p class="inbox-subject-3">Meeting notes from January 14th 2018</p>
      <p class="inbox-time-3">Jan 11</p>
      <p class="inbox-snippet-3">Snippet of the email content goes here...</p>
      <p class="inbox-attachment-3">important-presentation.pdf</p>

      <p class="inbox-names-4">Bethany, Melanie, Silvia</p>
      <p class="inbox-subject-4">A read email subject line</p>
      <p class="inbox-time-4">Jan 11</p>
      <p class="inbox-snippet-4">Snippet of the email content goes here...</p>
      <p class="inbox-attachment-4">ainsley-harriott.exe</p>

      <p class="inbox-names-5">Gautham Sajith</p>
      <p class="inbox-subject-5">A read email subject line</p>
      <p class="inbox-time-5">Jan 11</p>
      <p class="inbox-snippet-5">Snippet of the email content goes here...</p>

      <p class="inbox-names-6">Kunal Patel</p>
      <p class="inbox-subject-6">A read email subject line</p>
      <p class="inbox-time-6">Jan 10</p>
      <p class="inbox-snippet-6">Snippet of the email content goes here...</p>
      <img src="@/assets/images/014968643dd4978388219235ef393d9f067996cb-crop.png" alt="">
    </div>
  </div>
</template>

<script>
export default {
  name: 'Gmail',
  props: ['variables']
}
</script>

<style lang="scss" scoped>
  .inbox-names-1 {
    position: fixed;
    top: 15.5%;
    font-size: 1.75vh;
    text-align: left;
    padding-left: 4em;
    padding-right: 0.9em;
  }

  .inbox-subject-1 {
    position: fixed;
    top: 19%;
    font-size: 1.25vh;
    text-align: left;
    padding-left: 5.5em;
    padding-right: 1.75em;
  }

  .inbox-time-1 {
    position: fixed;
    top: 16%;
    left: 78.5%;
    font-size: 1vh;
    text-align: left;
    padding-left: 1.75em;
    // padding-right: 1.75em;
  }

  .inbox-attachment-1 {
    position: fixed;
    top: 22.5%;
    font-size: 1.25vh;
    text-align: left;
    padding-left: 5.5em;
    padding-right: 1.75em;
  }

  .inbox-names-2 {
    position: fixed;
    top: 28.5%;
    font-size: 1.75vh;
    text-align: left;
    padding-left: 4em;
    padding-right: 0.9em;
  }

  .inbox-subject-2 {
    position: fixed;
    top: 32%;
    font-size: 1.25vh;
    text-align: left;
    padding-left: 5.5em;
    padding-right: 1.75em;
  }

  .inbox-time-2 {
    position: fixed;
    top: 29%;
    left: 78.5%;
    font-size: 1vh;
    text-align: left;
    padding-left: 1.75em;
    // padding-right: 1.75em;
  }

  .inbox-snippet-2 {
    position: fixed;
    top: 34.5%;
    font-size: 1.25vh;
    text-align: left;
    padding-left: 5.5em;
    padding-right: 1.75em;
  }

  .inbox-names-3 {
    position: fixed;
    top: 40%;
    font-size: 1.75vh;
    text-align: left;
    padding-left: 4em;
    padding-right: 0.9em;
  }

  .inbox-subject-3 {
    position: fixed;
    top: 43.5%;
    font-size: 1.25vh;
    text-align: left;
    padding-left: 5.5em;
    padding-right: 1.75em;
  }

  .inbox-time-3 {
    position: fixed;
    top: 40.5%;
    left: 82.5%;
    font-size: 1vh;
    text-align: left;
    padding-left: 1.75em;
    // padding-right: 1.75em;
  }

  .inbox-snippet-3 {
    position: fixed;
    top: 46%;
    font-size: 1.25vh;
    text-align: left;
    padding-left: 5.5em;
    padding-right: 1.75em;
  }

  .inbox-attachment-3 {
    position: fixed;
    top: 49.5%;
    font-size: 1.25vh;
    text-align: left;
    padding-left: 5.5em;
    padding-right: 1.75em;
  }

  .inbox-names-4 {
    position: fixed;
    top: 54.5%;
    font-size: 1.75vh;
    text-align: left;
    padding-left: 4em;
    padding-right: 0.9em;
  }

  .inbox-subject-4 {
    position: fixed;
    top: 58%;
    font-size: 1.25vh;
    text-align: left;
    padding-left: 5.5em;
    padding-right: 1.75em;
  }

  .inbox-time-4 {
    position: fixed;
    top: 55%;
    left: 82.5%;
    font-size: 1vh;
    text-align: left;
    padding-left: 1.75em;
    // padding-right: 1.75em;
  }

  .inbox-snippet-4 {
    position: fixed;
    top: 60.5%;
    font-size: 1.25vh;
    text-align: left;
    padding-left: 5.5em;
    padding-right: 1.75em;
  }

  .inbox-attachment-4 {
    position: fixed;
    top: 64%;
    font-size: 1.25vh;
    text-align: left;
    padding-left: 5.5em;
    padding-right: 1.75em;
  }

  .inbox-names-5 {
    position: fixed;
    top: 70%;
    font-size: 1.75vh;
    text-align: left;
    padding-left: 4em;
    padding-right: 0.9em;
  }

  .inbox-subject-5 {
    position: fixed;
    top: 73.5%;
    font-size: 1.25vh;
    text-align: left;
    padding-left: 5.5em;
    padding-right: 1.75em;
  }

  .inbox-time-5 {
    position: fixed;
    top: 70.5%;
    left: 82.5%;
    font-size: 1vh;
    text-align: left;
    padding-left: 1.75em;
    // padding-right: 1.75em;
  }

  .inbox-snippet-5 {
    position: fixed;
    top: 76%;
    font-size: 1.25vh;
    text-align: left;
    padding-left: 5.5em;
    padding-right: 1.75em;
  }

  .inbox-names-6 {
    position: fixed;
    top: 80%;
    font-size: 1.75vh;
    text-align: left;
    padding-left: 4em;
    padding-right: 0.9em;
  }

  .inbox-subject-6 {
    position: fixed;
    top: 83.5%;
    font-size: 1.25vh;
    text-align: left;
    padding-left: 5.5em;
    padding-right: 1.75em;
  }

  .inbox-time-6 {
    position: fixed;
    top: 80.5%;
    left: 82%;
    font-size: 1vh;
    text-align: left;
    padding-left: 1.75em;
    // padding-right: 1.75em;
  }

  .inbox-snippet-6 {
    position: fixed;
    top: 86%;
    font-size: 1.25vh;
    text-align: left;
    padding-left: 5.5em;
    padding-right: 1.75em;
  }
</style>

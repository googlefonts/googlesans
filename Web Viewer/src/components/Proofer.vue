<template>
  <div class="main-container">
    <md-tabs @md-changed="tabChanged">
      <md-tab id="sentence-case" md-label="Sentence Case"></md-tab>
      <md-tab id="uppercase" md-label="Uppercase"></md-tab>
      <md-tab id="ui-elements" md-label="UI Elements"></md-tab>
    </md-tabs>
    <div :style="typefaceStyle" class="proofer-container google-text">
      <div v-if="currentTab !== 'ui-elements'" class="proofer-grid" :style="variables">
        <template v-for="size in ['20px','19px','18px','17px','16px','15px','14px','13px','12px','11px','10px']">
          <div class="proofer-paragraphs" :class="classObject">
            <p>Font-size: {{ size }}</p>
            <p :style="{'font-size': size}">
              Grumpy wizards make toxic brew for the evil Queen and Jack. One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed in his bed into a horrible vermin. He lay on his armour-like back, and if he lifted his head a little he could see his brown belly, slightly domed and divided by arches into stiff sections. The bedding was hardly able to cover it and seemed ready to slide off any moment. His many legs, pitifully thin compared with the size of the rest of him, waved about helplessly as he looked.
            </p>
          </div>
        </template>
      </div>
        <template v-if="currentTab === 'ui-elements'">
          <div :style="variables" class="ui-elements-container">


          <div class="ui-elements-group">
            <div class="separator">
              <md-avatar class="md-avatar-icon">G</md-avatar>
              <md-avatar class="md-avatar-icon md-primary">G</md-avatar>
              <md-avatar class="md-avatar-icon md-accent">G</md-avatar>
            </div>

            <div class="separator">
              <md-avatar class="md-avatar-icon md-small">PH</md-avatar>
              <md-avatar class="md-avatar-icon md-small md-primary">PH</md-avatar>
              <md-avatar class="md-avatar-icon md-small md-accent">PH</md-avatar>
            </div>

            <div class="separator">
              <md-avatar class="md-avatar-icon md-large">
                <md-ripple>OG</md-ripple>
              </md-avatar>

              <md-avatar class="md-avatar-icon md-large md-primary">
                <md-ripple>OG</md-ripple>
              </md-avatar>

              <md-avatar class="md-avatar-icon md-large md-accent">
                <md-ripple>OG</md-ripple>
              </md-avatar>
            </div>
          </div>

          <div class="ui-elements-group">
            <md-list class="md-list-proofer">
              <md-list-item>
                <md-icon>move_to_inbox</md-icon>
                <span class="md-list-item-text">Inbox</span>
                <md-badge class="md-primary md-square" md-content="6" />
              </md-list-item>

              <md-list-item>
                <md-icon>send</md-icon>
                <span class="md-list-item-text">Sent Mail</span>
              </md-list-item>

              <md-list-item>
                <md-icon>delete</md-icon>
                <span class="md-list-item-text">Trash</span>
                <md-badge class="md-primary" md-content="6" />
              </md-list-item>

              <md-list-item>
                <md-icon>error</md-icon>
                <span class="md-list-item-text">Spam</span>
                <md-badge class="md-square" md-content="New" />
              </md-list-item>
            </md-list>
          </div>

          <div class="ui-elements-group ui-elements-group-buttons">
            <div>
              <!-- <small>Flat</small> -->
              <md-button>Default</md-button>
              <md-button class="md-buttons-proofer" :md-ripple="false">Ripple Off</md-button>
              <md-button class="md-buttons-proofer md-primary">Primary</md-button>
              <md-button class="md-buttons-proofer md-accent">Accent</md-button>
              <md-button class="md-buttons-proofer" disabled>Disabled</md-button>
            </div>

            <div>
              <!-- <small>Raised</small> -->
              <md-button class="md-buttons-proofer md-raised">Default</md-button>
              <md-button class="md-buttons-proofer md-raised" :md-ripple="false">Ripple Off</md-button>
              <md-button class="md-buttons-proofer md-raised md-primary">Primary</md-button>
              <md-button class="md-buttons-proofer md-raised md-accent">Accent</md-button>
              <md-button class="md-buttons-proofer md-raised" disabled>Disabled</md-button>
            </div>

            <div>
              <!-- <small>Dense</small> -->
              <md-button class="md-buttons-proofer md-dense md-primary">Flat</md-button>
              <md-button class="md-buttons-proofer md-dense md-raised md-primary">Raised</md-button>
            </div>
          </div>

          <div class="ui-elements-group">
            <md-card class="md-card-example">
              <md-card-area md-inset>
                <md-card-media md-ratio="16:9">
                  <img src="https://upload.wikimedia.org/wikipedia/commons/f/fd/Caf%C3%A9_de_Flore.jpg" alt="Coffee House">
                </md-card-media>

                <md-card-header>
                  <h2 class="md-title">Coffee House</h2>
                  <div class="md-subhead">
                    <md-icon>location_on</md-icon>
                    <span>2 miles</span>
                  </div>
                </md-card-header>

                <md-card-content>
                  Illy Coffee served with a complimentary Leonidas Belgian Chocolate with all beverages.
                </md-card-content>
              </md-card-area>

              <md-card-content>
                <h3 class="md-subheading">Today's availability</h3>
                <div class="card-reservation">
                  <md-icon>access_time</md-icon>
                  <div class="md-button-group">
                    <md-button>5:30PM</md-button>
                    <md-button>7:30PM</md-button>
                    <md-button>9:00PM</md-button>
                  </div>
                </div>
              </md-card-content>

              <md-card-actions>
                <md-button class="md-primary">Reserve</md-button>
              </md-card-actions>
            </md-card>
          </div>

          <div class="ui-elements-group">
            <div class="viewport">
                  <md-toolbar :md-elevation="1">
                    <span class="md-title">Default</span>
                  </md-toolbar>

                  <md-list class="md-double-line">
                    <md-subheader>Phone</md-subheader>

                    <md-list-item>
                      <md-icon class="md-primary">phone</md-icon>

                      <div class="md-list-item-text">
                        <span>(650) 555-1234</span>
                        <span>Mobile</span>
                      </div>

                      <md-button class="md-icon-button md-list-action">
                        <md-icon>sms</md-icon>
                      </md-button>
                    </md-list-item>

                    <md-list-item class="md-inset">
                      <div class="md-list-item-text">
                        <span>(650) 555-1234</span>
                        <span>Mobile</span>
                      </div>

                      <md-button class="md-icon-button md-list-action">
                        <md-icon>sms</md-icon>
                      </md-button>
                    </md-list-item>

                    <md-divider></md-divider>
                    <md-subheader>Email</md-subheader>

                    <md-list-item>
                      <md-icon class="md-primary">email</md-icon>

                      <div class="md-list-item-text">
                        <span>aliconnors@example.com</span>
                        <span>Personal</span>
                      </div>
                    </md-list-item>

                    <md-list-item class="md-inset">
                      <div class="md-list-item-text">
                        <span>ali_connors@example.com</span>
                        <span>Work</span>
                      </div>
                    </md-list-item>
                  </md-list>
                </div>

                <div class="viewport">
                  <md-toolbar :md-elevation="1">
                    <span class="md-title">Primary</span>
                  </md-toolbar>

                  <md-list>
                    <md-subheader class="md-primary">Navigation</md-subheader>

                    <md-list-item>
                      <md-icon>move_to_inbox</md-icon>
                      <span class="md-list-item-text">Inbox</span>
                    </md-list-item>

                    <md-list-item>
                      <md-icon>send</md-icon>
                      <span class="md-list-item-text">Sent Mail</span>
                    </md-list-item>

                    <md-list-item>
                      <md-icon>delete</md-icon>
                      <span class="md-list-item-text">Trash</span>
                    </md-list-item>

                    <md-list-item>
                      <md-icon>error</md-icon>
                      <span class="md-list-item-text">Spam</span>
                    </md-list-item>
                  </md-list>

                    <md-divider></md-divider>

                  <md-list>
                    <md-subheader class="md-primary">Contacts</md-subheader>

                    <md-list-item>
                      <md-avatar>
                        <img src="https://placeimg.com/40/40/people/5" alt="People">
                      </md-avatar>

                      <span class="md-list-item-text">Abbey Christansen</span>

                      <md-button class="md-icon-button md-list-action">
                        <md-icon class="md-primary">chat_bubble</md-icon>
                      </md-button>
                    </md-list-item>

                    <md-list-item>
                      <md-avatar>
                        <img src="https://placeimg.com/40/40/people/1" alt="People">
                      </md-avatar>

                      <span class="md-list-item-text">Alex Nelson</span>

                      <md-button class="md-icon-button md-list-action">
                        <md-icon class="md-primary">chat_bubble</md-icon>
                      </md-button>
                    </md-list-item>

                    <md-list-item>
                      <md-avatar>
                        <img src="https://placeimg.com/40/40/people/6" alt="People">
                      </md-avatar>

                      <span class="md-list-item-text">Mary Johnson</span>

                      <md-button class="md-icon-button md-list-action">
                        <md-icon>chat_bubble</md-icon>
                      </md-button>
                    </md-list-item>
                  </md-list>
                </div>
              </div>


          </div>
        </template>

    </div>
  </div>
</template>

<script>
export default {
  name: 'Proofer',
  props: ['variables', 'typefaceStyle'],
  data() {
    return {
      currentTab: 'sentence-case'
    }
  },
  computed: {
    classObject() {
      if (this.currentTab === 'uppercase') {
        return {
          uppercase: true
        }
      } else {
        return {
          'sentence-case': true
        }
      }
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

.ui-elements-container {
  margin: 4em 4em 4em 6em;
  &:last-child {
    margin-bottom: 4em;
  }
}

.ui-elements-group {
  // display: inline-block;
  padding-bottom: 2em;
  padding-right: 2em;
  .md-card {
    margin: 0;
  }
  .viewport {
    margin-right: 2em;
  }
  .md-buttons-proofer {
    margin-bottom: 2em;
    margin-right: 2em;
  }
  &:last-child {
    margin-bottom: 4em;
  }
}

.ui-elements-group-buttons {
  margin-bottom: -2em;
}

.md-avatar-icon {
  margin-right: 12px;
}

.separator + .separator {
  margin-top: 24px;
}

small {
  display: block;
}

.md-list {
width: 320px;
max-width: 100%;
display: inline-block;
vertical-align: top;
}

.md-list-proofer {
  border: 1px solid rgba(#000, .12);
}

  .md-card {
    width: 320px;
    margin: 4px;
    display: inline-block;
    vertical-align: top;
  }

  .md-card-example {
    .md-subhead {
      .md-icon {
        $size: 16px;

        width: $size;
        min-width: $size;
        height: $size;
        font-size: $size !important;
      }

      span {
        vertical-align: middle;
      }
    }

    .card-reservation {
      margin-top: 8px;
      display: flex;
      align-items: center;
      justify-content: space-between;

      .md-icon {
        margin: 8px;
      }
    }

    .md-button-group {
      display: flex;

      .md-button {
        min-width: 60px;
        border-radius: 2px;
      }
    }
  }
</style>

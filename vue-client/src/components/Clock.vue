<script>
export default {
  data() {
    return {
      formattedTime: '',
      formattedDate: '',
      greeting: '',
      iconPath: '',
      iconAlt: ''
    };
  },
  mounted() {
    this.updateTime();
    setInterval(this.updateTime, 60000); // 1 minute
  },
  methods: {
    updateTime() {
      const now = new Date();
      const timeOptions = {
        hour: 'numeric',
        minute: 'numeric'
      };
      this.formattedTime = now.toLocaleString('pt-PT', timeOptions);
      const dateOptions = {
        weekday: 'long',
        day: 'numeric',
        month: 'long',
        year: 'numeric'
      };
      this.formattedDate = now.toLocaleString('pt-PT', dateOptions);
      const hour = now.getHours();
      if (hour >= 5 && hour < 12) {
        this.greeting = 'Bom dia!';
        this.iconPath = '../src/assets/sun.png';
        this.iconAlt = 'Sol';
      } else if (hour >= 12 && hour < 18) {
        this.greeting = 'Boa tarde!';
        this.iconPath = '../src/assets/sun.png';
        this.iconAlt = 'Sol';
      } else {
        this.greeting = 'Boa noite!';
        this.iconPath = '../src/assets/moon.png';
        this.iconAlt = 'Lua';
      }
    }
  }
};
</script>

<template>
  <div class="clock-container">
    <div class="greeting-container">
      <span class="greeting">{{ greeting }}</span>
      <img :src="iconPath" :alt="iconAlt" class="daytime-icon">
    </div>
    <div class="date-container">
      <div class="clock-time">{{ formattedTime }}</div>
      <div class="clock-date">{{ formattedDate }}</div>
    </div>
  </div>
</template>

<style scoped>
.clock-container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.greeting-container {
  display: flex;
  flex-direction: column;
  text-align: left;
}

.date-container {
  display: flex;
  flex-direction: column;
  text-align: right;
}

.greeting,
.clock-time {
  font-size: 30px;
  font-weight: bold;
}

.clock-date {
  font-size: 18px;
}

.daytime-icon {
  height: 24px;
  width: 24px;
}
</style>

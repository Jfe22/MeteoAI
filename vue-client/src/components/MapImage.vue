<script>
import axios from "axios";

export default {
  name: "MapImage",
  data() {
    return {
      radarImages: [],
      currentImgIndex: 0,
    };
  },
  async mounted() {
    this.getRadarImages();
  },
  methods: {
    getRadarImages() {
      console.log("Getting radar images...");
      axios
          .get("http://localhost:5000/radar-images")
          .then((response) => {
            const data = response.data;
            this.radarImages = [
              `data:image/png;base64,${data.image1}`,
              `data:image/png;base64,${data.image2}`,
              `data:image/png;base64,${data.image3}`,
            ];
            this.currentImgIndex = 2;
            console.log("Radar images received!");
          })
          .catch((error) => {
            console.log(error);
          });
    },
    nextImage() {
      if (this.currentImgIndex < this.radarImages.length - 1) {
        this.currentImgIndex++;
      }
    },
    prevImage() {
      if (this.currentImgIndex > 0) {
        this.currentImgIndex--;
      }
    },
  },
};
</script>

<template>
  <div class="map-container">
    <img src="../assets/mapaPortugal.png" alt="Mapa" class="map-image"  />
    <img :src="radarImages[currentImgIndex]" alt="Imagem Radar" class="radar-image" />
    <div class="slider-controls">
      <button @click="prevImage" :disabled="currentImgIndex === 0">‹</button>
      <button @click="nextImage" :disabled="currentImgIndex === radarImages.length - 1">›</button>
    </div>
  </div>
</template>

<style scoped>
.map-container {
  height: 95vh;
  width: calc(95vh * (1153 / 1713));
  position: relative;
  overflow: hidden;
}

.map-image {
  height: 100%;
  width: auto;
  display: block;
}

.radar-image {
  position: absolute;
  top: -32%;
  left: -37%;
  width: 180%;
  height: 184%;
}

.slider-controls {
  position: absolute;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 10px;
}

button {
  background-color: black;
  color: white;
  opacity: 80%;
  border: none;
  padding: 8px 14px;
  font-size: 18px;
  border-radius: 8px;
  cursor: pointer;
}

button:disabled {
  opacity: 20%;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  opacity: 60%;
}
</style>

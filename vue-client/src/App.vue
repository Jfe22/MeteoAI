<script>
import Clock from "./components/Clock.vue";
import MapImage from "./components/MapImage.vue";
import PredictionsTable from "./components/PredictionsTable.vue";

export default {
  name: "App",
  components: {
    Clock,
    MapImage,
    PredictionsTable,
  },
};
</script>

<template>
  <div class="app-container">
    <header>
      <Clock ref="clock" />
    </header>

    <main>
      <div class="table-wrapper">
        <PredictionsTable ref="predictions" />
      </div>
      <div class="map-wrapper">
        <MapImage ref="map" />
      </div>
    </main>

    <footer>
      <h5>Projeto Web Meteo com Inteligência Artificial</h5>
      <h5>Desenvolvido por:</h5>
      <p>
        José Ferreira - 2181706
        <br />
        Rúben Antunes - 2170957
      </p>
    </footer>
  </div>
</template>

<style scoped>
header {
  background-color: var(--vt-c-sand);
  color: var(--vt-c-darkblue);
  margin-bottom: 20px;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
}

main {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.table-wrapper,
.map-wrapper {
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
}

footer {
  text-align: center;
  background-color: var(--vt-c-sand);
  color: var(--vt-c-darkblue);
  margin-top: 20px;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
}

@media (min-width: 768px) {
  main {
    flex-direction: row;
  }

  main {
    max-height: 95vh;
  }

  .table-wrapper,
  .map-wrapper {
    max-height: 100%;
  }
}
</style>

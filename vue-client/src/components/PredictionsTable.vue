<script>
import axios from "axios";

export default {
  name: "PredictionsTable",
  data() {
    return {
      formattedData: {},
      isLoading: true,
      time_delay1h: "",
      time_delay2h: "",
      time_delay3h: "",
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      this.isLoading = true;
      this.formattedData = {};
      this.time_delay1h = "";
      this.time_delay2h = "";
      this.time_delay3h = "";
      console.log("Fetching data...");
      axios
          .get("http://localhost:5000/predict-rain")
          .then((response) => {
            const data = response.data;
            for (const [key, value] of Object.entries(data)) {
              for (const [key2, value2] of Object.entries(value)) {
                if (!this.formattedData[key2]) {
                  this.formattedData[key2] = [];
                }
                this.formattedData[key2].push(value2);
              }
            }
            this.isLoading = false;
            console.log(this.formattedData);
            // Obter a hora atual em UTC
            var current_datetime_utc = new Date();
            // Arredondar a hora atual para o múltiplo de 5 mais próximo
            var rounded_datetime = new Date(current_datetime_utc);
            rounded_datetime.setMinutes(
                Math.floor(rounded_datetime.getMinutes() / 5) * 5
            );
            // Atrasar a hora em 10 minutos
            var datetime_delay = new Date(
                rounded_datetime.getTime() - 10 * 60000 + 3600000
            );
            // Converter a hora para o formato hh:mm
            this.time_delay1h = datetime_delay.toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
            });
            this.time_delay2h = new Date(
                datetime_delay.getTime() + 3600000
            ).toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
            });
            this.time_delay3h = new Date(
                datetime_delay.getTime() + 2 * 3600000
            ).toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
            });
          })
          .catch((error) => {
            console.error(error);
          });
    },
    getStyle(value) {
      switch (value) {
        case 0:
          return { backgroundColor: 'var(--vt-c-warning-green)' }; // Sem Chuva
        case 1:
          return { backgroundColor: 'var(--vt-c-warning-yellow)' }; // Chuva Fraca
        case 2:
          return { backgroundColor: 'var(--vt-c-warning-orange)' }; // Chuva Moderada
        case 3:
          return { backgroundColor: 'var(--vt-c-warning-red)' }; // Chuva Forte
        default:
          return {};
      }
    },
  },
};
</script>

<template>
  <div v-if="isLoading" class="text-placeholder">
    <p>A calcular previsões...</p>
  </div>
  <div v-else class="table-container">
    <table class="table-data">
      <thead>
      <tr>
        <th>Distrito</th>
        <th>Previsão para as {{ time_delay1h }}</th>
        <th>Previsão para as {{ time_delay2h }}</th>
        <th>Previsão para as {{ time_delay3h }}</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(item, key) in formattedData" :key="key">
        <td>{{ key }}</td>
        <td :style="getStyle(item[0])"></td>
        <td :style="getStyle(item[1])"></td>
        <td :style="getStyle(item[2])"></td>
      </tr>
      </tbody>
    </table>
    <div class="table-legends">
      <h3>Legenda</h3>
      <ul>
        <li><span class="color-box" style="background-color: var(--vt-c-warning-green);"></span> &lt; 0,1 mm/h (Sem Chuva)</li>
        <li><span class="color-box" style="background-color: var(--vt-c-warning-yellow);"></span> 0,1 a 0,49 mm/h (Chuva Fraca)</li>
        <li><span class="color-box" style="background-color: var(--vt-c-warning-orange);"></span> 0,5 a 3,99 mm/h (Chuva Moderada)</li>
        <li><span class="color-box" style="background-color: var(--vt-c-warning-red);"></span> &gt; 4 mm/h (Chuva Forte)</li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.text-placeholder {
  text-align: center;
}

.table-container {
  display: flex;
  flex-direction: column;
}

.table-data {
  background-color: var(--vt-c-darkblue);
  color: var(--vt-c-white);
  flex: 1;
}

.table-data th {
  background-color: var(--vt-c-blue);
  font-weight: bold;
}

.table-data td {
  text-align: center;
}

.table-data tr:nth-child(even) td {
  background-color: var(--vt-c-blue);
}

.table-data tr:nth-child(odd) td {
  background-color: var(--vt-c-darkblue);
}

.table-legends {
  background-color: var(--vt-c-darkblue);
  color: var(--vt-c-white);
  padding: 10px;
}

.table-legends li {
  list-style-type: none;
}

.color-box {
  display: inline-block;
  width: 20px;
  height: 20px;
  margin-right: 5px;
}

@media (prefers-color-scheme: dark) {
  .table-data {
    background-color: var(--vt-c-blue);
    color: var(--vt-c-white);
  }

  .table-data th {
    background-color: var(--vt-c-darkblue);
  }

  .table-data tr:nth-child(even) td {
    background-color: var(--vt-c-darkblue);
  }

  .table-data tr:nth-child(odd) td {
    background-color: var(--vt-c-blue);
  }

  .table-legends {
    background-color: var(--vt-c-blue);
    color: var(--vt-c-white);
  }
}

@media (min-width: 768px) {
  .table-container {
    height: 100%;
    overflow-y: auto;
  }
}
</style>

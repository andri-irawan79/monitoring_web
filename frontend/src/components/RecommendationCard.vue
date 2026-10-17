<template>
  <div class="recommendation-card">

    <h2>🌱 Rekomendasi Pupuk</h2>

    <div v-if="recommendation">

      <p>
        <strong>Jenis Pupuk :</strong>
        {{ recommendation.jenis_pupuk }}
      </p>

      <p>
        <strong>Dosis :</strong>
        {{ recommendation.dosis }}
        kg/pohon/tahun
      </p>

      <p>
        <strong>Kategori :</strong>
        {{ recommendation.kategori }}
      </p>

    </div>

    <div v-else>
      Belum ada rekomendasi.
    </div>

  </div>
</template>

<script setup>

defineProps({
  recommendation: Object
})

</script>

<style scoped>

.recommendation-card {

  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);

}

</style>

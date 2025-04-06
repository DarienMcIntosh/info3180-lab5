<template>
    <div class="add-movie-view">
      <h1>Add New Movie</h1>
      <MovieForm />
    </div>
</template>
  
  <script>
  import MovieForm from '@/components/MovieForm.vue';
  
  export default {
    name: 'AddMovieFormView',
    components: {
      MovieForm
    }
  }
  </script>
  
  <style scoped>
  .add-movie-view {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }
  
  h1 {
    margin-bottom: 20px;
  }
  </style>
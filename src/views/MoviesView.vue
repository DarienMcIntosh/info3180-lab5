<template>
    <div class="container mt-5">
      <h2 class="mb-4">Movie List</h2>
      
      <div v-if="loading" class="text-center">
        <p>Loading movies...</p>
      </div>
      
      <div v-else-if="error" class="alert alert-danger">
        {{ error }}
      </div>
      
      <div v-else-if="movies.length === 0" class="alert alert-info">
        No movies available. Add some movies first!
      </div>
      
      <div v-else class="row row-cols-1 row-cols-md-3 g-4">
        <div v-for="movie in movies" :key="movie.id" class="col">
          <div class="card h-100">
            <!-- Apply the 'movie-poster' class to the img tag -->
            <img 
              :src="movie.poster" 
              class="card-img-top movie-poster" 
              :alt="movie.title"
            >
            <div class="card-body">
              <h5 class="card-title">{{ movie.title }}</h5>
              <p class="card-text">{{ movie.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  
  const movies = ref([]);
  const loading = ref(true);
  const error = ref(null);
  
  function fetchMovies() {
    fetch('/api/v1/movies')
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch movies');
        }
        return response.json();
      })
      .then(data => {
        movies.value = data.movies;
        loading.value = false;
      })
      .catch(err => {
        console.error('Error fetching movies:', err);
        error.value = 'Unable to load movies. Please try again later.';
        loading.value = false;
      });
  }
  
  onMounted(() => {
    fetchMovies();
  });
  </script>

<style scoped>
.movie-poster {
  width: 100%; /* Ensure the image spans the full width of its container */
  height: 200px; /* Set a fixed height for all images */
  object-fit: cover; /* Scale and crop the image to fill the container while maintaining aspect ratio */
  object-position: center; /* Center the image within the container */
}
</style>
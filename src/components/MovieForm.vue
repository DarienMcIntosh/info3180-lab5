<template>
  <div class="container mt-5">
    <h2>Upload Movie</h2>
    <form @submit.prevent="saveMovie" id="movieForm">
      <!-- Movie Title -->
      <div class="form-group mb-3">
        <label for="title" class="form-label">Movie Title</label>
        <input
          type="text"
          id="title"
          name="title"
          v-model="movie.title"
          class="form-control"
          required
        />
      </div>

      <!-- Movie Description -->
      <div class="form-group mb-3">
        <label for="description" class="form-label">Description</label>
        <textarea
          id="description"
          name="description"
          v-model="movie.description"
          class="form-control"
          rows="4"
          required
        ></textarea>
      </div>

      <!-- Movie Poster -->
      <div class="form-group mb-3">
        <label for="poster" class="form-label">Poster</label>
        <input
          type="file"
          id="poster"
          name="poster"
          @change="handleFileUpload"
          class="form-control"
          required
        />
      </div>

      <!-- Submit Button -->
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>

    <!-- Response Message -->
    <div v-if="responseMessage" class="mt-3 alert alert-success">
      {{ responseMessage }}
    </div>

    <!-- Error Messages -->
    <div v-if="errors.length > 0" class="mt-3 alert alert-danger">
      <ul>
        <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

// Reactive data for form fields and response handling
const movie = ref({
  title: '',
  description: '',
  poster: null,
});
const responseMessage = ref('');
const errors = ref([]);
const csrf_token = ref('');

function getCsrfToken() {
  fetch('/api/v1/csrf-token')
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      csrf_token.value = data.csrf_token;
    });
}

onMounted(() => {
  getCsrfToken();
});


// Handle file upload
const handleFileUpload = (event) => {
  movie.value.poster = event.target.files[0];
};

// Save movie using Fetch API
const saveMovie = () => {
  let movieForm = document.getElementById('movieForm');
  let form_data = new FormData(movieForm);
  
  fetch("/api/v1/movies", {
    method: 'POST',
    body: form_data,
    headers: {
      'X-CSRFToken': csrf_token.value
    }
  })
  .then(function (response) {
    return response.json();
  })
  .then(function (data) {
    // display a success message
    console.log(data);
    responseMessage.value = data.message;
    errors.value = [];
    movie.value = { title: '', description: '', poster: null };
  })
  .catch(function (error) {
    console.log(error);
    errors.value = ['An error occurred while processing the request.'];
  });
};
</script>

<style scoped>
.container{
  margin: 0 auto;
  padding: 20px;
  border-radius: 20px;
  border: 2px #007bff;
  box-shadow: 0 0 3px 3px #007bff2e;
}

h2{
  text-align: center;
}

</style>

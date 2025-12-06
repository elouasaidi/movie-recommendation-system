$(document).ready(function() {
  // Cacher le formulaire d'inscription au chargement de la page
  $(".form--signup").hide();

  // Action lorsque le bouton "S'inscrire" est cliqué
  $("#signupBtn").click(function() {
    $(".form--signup").show();
    $(".form--login").hide();
  });

  // Action lorsque le bouton "Connecter" est cliqué
  $("#loginBtn").click(function() {
    $(".form--signup").hide();
    $(".form--login").show();
  });
});


document.getElementById("closeForm").addEventListener("click", function() {
  document.querySelector(".form--login").style.display = "none";
  document.querySelector(".form--signup").style.display = "none";
  document.querySelector(".container").style.display = "none";
  document.querySelector(".sidebar").style.display = "block";
});

const userProfileBtn = document.getElementById('user-profile').querySelector('a');
userProfileBtn.addEventListener('click', function(event) {
  event.preventDefault(); // Prevent default link behavior
  // Redirect to the profile page
  window.location.href = 'profile.html';
});

$(document).ready(function() {
  var message = "{{ message }}";
  if (message) {
      // Choisir la classe appropriée en fonction du type de message
      var messageType = "{{ message_type }}"; // Vous devez avoir un moyen de déterminer le type de message (succès, erreur, avertissement, etc.)
      var alertClass = "";
      if (messageType === "success") {
          alertClass = "alert-success";
      } else if (messageType === "error") {
          alertClass = "alert-error";
      } else if (messageType === "warning") {
          alertClass = "alert-warning";
      }
      // Afficher le message d'alerte avec la classe appropriée
      $('#alert-message').text(message).addClass(alertClass).show();
  }
});
var alertMessage = document.getElementById('alert-message');

// Fonction pour afficher l'alerte de succès
function showSuccessMessage(message) {
    alertMessage.innerHTML = message; // Ajoute le message à l'alerte
    alertMessage.classList.add('alert-success'); // Ajoute la classe pour le style de succès
    alertMessage.style.display = 'block'; // Affiche l'alerte
}
document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('search-input');
  const searchForm = document.getElementById('search-form');

  searchForm.addEventListener('submit', (event) => {
      event.preventDefault(); // Empêcher le formulaire de soumettre normalement

      // Récupérer la valeur de la barre de recherche
      const searchQuery = searchInput.value.trim();
      if (searchQuery !== '') {
          // Soumettre le formulaire avec le terme de recherche
          window.location.href = `/recommend?search-term=${encodeURIComponent(searchQuery)}`;
      }
  });
});


<?php 
// Insère le message reçu avec $_POST dans la BDD
// Redirige vers formulaire.html
// Cette page ne sera jamais visible par l'utilisateur.

// Pas de détail d'erreur
error_reporting(0);

// Effectuer ici la requête qui insère le message
require("connexion_bdd.php");
require("nettoyer.php");

// Vérifie présence de tous les paramètres
if (isset($_POST['pseudo']) AND isset($_POST['mail']) AND isset($_POST['nom_spot']) AND isset($_POST['date_visite']) AND isset($_POST['commentaire']))
{
  // Nettoyage entrées utilisateur
  $pseudo = nettoyer($_POST['pseudo']);
  $mail = nettoyer($_POST['mail']);
  $nom_spot = nettoyer($_POST['nom_spot']);
  $date_visite = nettoyer($_POST['date_visite']);
  $commentaire = nettoyer($_POST['commentaire']);

  // Requête
  $req = $bdd->prepare('INSERT INTO kitesurf(pseudo, mail, nom_spot, date_visite, commentaire) VALUES (:pseudo, :mail, :nom_spot, :date_visite, :commentaire)');
  $req->execute(array(
    'pseudo' => $pseudo,
    'mail' => $mail,
    'nom_spot' => $nom_spot,
    'date_visite' => $date_visite,
    'commentaire' => $commentaire
  ));
}
// Redirection
header('Location: ../formulaire.php#commentaires');
?>
<?php 
  // Pas de détail d'erreur
  error_reporting(0);

  // Connexion à la base de données

  // Variables
  $servername = "servername";
  $database = "database";
  $username = "username";
  $password = "password";

  try{
    $bdd = new PDO("mysql:host=$servername; dbname=$database; charset=utf8", $username, $password);
    // Erreurs verbeuses
    $bdd->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    // echo 'Connexion BDD OK.';
  }
  catch (Exception $e)
  {
    die('Erreur : ' . $e->getMessage());
  }
?>

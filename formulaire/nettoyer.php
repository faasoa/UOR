<?php 
  // Pas de détail d'erreur
  error_reporting(0);

  function nettoyer($chaine)
  {
    if ($chaine)
    {
      $chaine = trim($chaine);
      $chaine = stripslashes($chaine);
      $chaine = htmlspecialchars($chaine);
    }
    return $chaine;
  }
?>
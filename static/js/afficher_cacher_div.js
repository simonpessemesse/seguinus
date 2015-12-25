function afficher_cacher(id)
{
        if(document.getElementById(id).style.visibility=="hidden")
        {
                document.getElementById(id).style.visibility="visible";
                document.getElementById('bouton_'+id).innerHTML='Cacher le texte';
        }
        else
        {
                document.getElementById(id).style.visibility="hidden";
                document.getElementById('bouton_'+id).innerHTML='Afficher le texte';
        }
        return true;
}


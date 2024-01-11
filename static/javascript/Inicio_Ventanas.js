function entrar() {
    elemento = document.getElementById("IniSes");
    elemento.style.visibility = "visible";
}
function registrar() {
    elemento = document.getElementById("Reg");
    elemento.style.visibility = "visible";
}
function SaleSes() {
    elemento = document.getElementById("IniSes");
    elemento.style.visibility = "hidden";
}
function SaleReg() {
    elemento = document.getElementById("Reg");
    elemento.style.visibility = "hidden";
}

$('#Texto_cargar').hide();

function CargarCsv() {
    Cargar_Csv = $('#CSV').show();
    Escribir_Elemento = $('#Texto_cargar').hide();
}
function Ingresar_texto() {
    Cargar_Csv = $('#CSV').hide();
    Escribir_Elemento = $('#Texto_cargar').show();
}
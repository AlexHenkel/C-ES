goog.provide('Blockly.Blocks.custom');
goog.require('Blockly.Blocks');

// ********** Iniciar programa **********

Blockly.Blocks['programa'] = {
   init: function () {
      this.appendDummyInput().appendField("Programa");
      this.appendStatementInput("VAR_AND_FUNCS").setCheck(["VARIABLES", "FUNCTIONS"]);
      this.appendStatementInput("MAIN").setCheck(null);
      this.setColour("#009494");
      this.setTooltip('Con este bloque se declara el inicio del programa');
   }
};


// ********** Declaración de variables **********

Blockly.Blocks['init_variables'] = {
   init: function () {
      this.appendDummyInput().appendField("Variables:")
      this.setPreviousStatement(true, "VARIABLES");
      this.setNextStatement(true, "VARIABLE");
      this.setColour("#F35B05");
      this.setTooltip('En este bloque se declaran las variables globales');
   }
};

Blockly.Blocks['declare_variable'] = {
   init: function () {
      this.appendValueInput("INPUT").setCheck("OTHER_VARIABLE")
      .appendField(new Blockly.FieldDropdown([["numero", "numero"], ["decimal", "decimal"], ["texto", "texto"], ["binario", "binario"]]), "TYPE")
      .appendField(new Blockly.FieldTextInput("nombreVariable"), "NAME");
      this.setPreviousStatement(true, "VARIABLE");
      this.setNextStatement(true, "VARIABLE");
      this.setColour("#F38C13");
      this.setTooltip('Declaración de una variable');
   }
};

Blockly.Blocks['one_more_variable'] = {
   init: function () {
      this.appendValueInput("INPUT").setCheck("OTHER_VARIABLE")
         .appendField(", ")
         .appendField(new Blockly.FieldTextInput("otraVariable"), "NAME");
      this.setOutput(true, "OTHER_VARIABLE");
      this.setColour("#F38C13");
      this.setTooltip('Declaración de otra variable');
   }
};

Blockly.Blocks['declare_array'] = {
   init: function () {
      this.appendValueInput("INPUT").setCheck("OTHER_ARRAY")
         .appendField("lista de ")
         .appendField(new Blockly.FieldDropdown([["numero", "numero"], ["decimal", "decimal"], ["texto", "texto"], ["binario", "binario"]]), "TYPE")
         .appendField("de ")
         .appendField(new Blockly.FieldNumber(1, 1), "SIZE")
         .appendField(new Blockly.FieldTextInput("nombreLista"), "NAME");
      this.setPreviousStatement(true, "VARIABLE");
      this.setNextStatement(true, "VARIABLE");
      this.setColour("#F0B90C");
      this.setTooltip('Declaración de una lista');
   }
};

Blockly.Blocks['one_more_array'] = {
   init: function () {
      this.appendValueInput("INPUT").setCheck("OTHER_ARRAY")
         .appendField(", ")
         .appendField(new Blockly.FieldTextInput("otraLista"), "NAME");
      this.setOutput(true, "OTHER_ARRAY");
      this.setColour("#F0B90C");
      this.setTooltip('Declaración de otra lista');
   }
};


// ********** Declaración de funciones **********

Blockly.Blocks['init_functions'] = {
   init: function () {
      this.appendDummyInput().appendField("Funciones:")
      this.setPreviousStatement(true, ["FUNCTIONS", "VARIABLE"]);
      this.setNextStatement(true, "FUNCTION");
      this.setColour("#660A3E");
      this.setTooltip('En este bloque se declaran las funciones');
   }
}
Blockly.Blocks['function_with_params'] = {
   init: function () {
      this.appendValueInput("PARAMETERS").setCheck('OTHER_PARAM')
         .appendField("Regresa: ")
         .appendField(new Blockly.FieldDropdown([["nada", "nada"], ["numero", "numero"], ["decimal", "decimal"], ["texto", "texto"], ["binario", "binario"]]), "TYPE")
         .appendField("Nombre: ")
         .appendField(new Blockly.FieldTextInput("nombreFunción"), "NAME")
         .appendField("Parámetros:");
      this.appendStatementInput("BODY_FUNCTION").setCheck(["BODY_FUNCTION", "LOCAL_VARIABLES", "STATEMENT"]);
      this.setPreviousStatement(true, "FUNCTION");
      this.setNextStatement(true, "FUNCTION");
      this.setColour("#891C56");
   }
};

Blockly.Blocks['function_param'] = {
   init: function () {
      this.appendValueInput("PARAMETERS").setCheck("OTHER_PARAM")
         .appendField(new Blockly.FieldDropdown([["numero", "numero"], ["decimal", "decimal"], ["texto", "texto"], ["binario", "binario"]]), "TYPE")
         .appendField(new Blockly.FieldTextInput("nombreParámetro"), "NAME");
      this.setOutput(true, "OTHER_PARAM");
      this.setColour("#891C56");
   }
};

Blockly.Blocks['function_without_params'] = {
   init: function () {
      this.appendDummyInput()
         .appendField("Regresa: ")
         .appendField(new Blockly.FieldDropdown([["nada", "nada"], ["numero", "numero"], ["decimal", "decimal"], ["texto", "texto"], ["binario", "binario"]]), "TYPE")
         .appendField("Nombre: ")
         .appendField(new Blockly.FieldTextInput("nombreFunción"), "NAME");
      this.appendStatementInput("BODY_FUNCTION").setCheck(["BODY_FUNCTION", "LOCAL_VARIABLES", "STATEMENT"]);
      this.setPreviousStatement(true, "FUNCTION");
      this.setNextStatement(true, "FUNCTION");
      this.setColour("#B0276F");
   }
};

Blockly.Blocks['return'] = {
   init: function () {
      this.appendValueInput("RETURN")
         .setCheck(null)
         .appendField("Regresar:");
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour("#B0276F");
   }
};


// ********** Declaración de variables locales **********

Blockly.Blocks['init_local_variables'] = {
   init: function () {
      this.appendDummyInput().appendField("Variables locales:")
      this.setPreviousStatement(true, "LOCAL_VARIABLES");
      this.setNextStatement(true, ["VARIABLE_LOCAL", "STATEMENT"]);
      this.setColour("#C93482");
      this.setTooltip('En este bloque se declaran las variables globales');
   }
};

Blockly.Blocks['declare_local_variable'] = {
   init: function () {
      this.appendValueInput("INPUT").setCheck("OTHER_LOCAL_VARIABLE")
         .appendField(new Blockly.FieldDropdown([["numero", "numero"], ["decimal", "decimal"], ["texto", "texto"], ["binario", "binario"]]), "TYPE")
         .appendField(new Blockly.FieldTextInput("nombreVariable"), "NAME");
      this.setPreviousStatement(true, "VARIABLE_LOCAL");
      this.setNextStatement(true, ["VARIABLE_LOCAL", "STATEMENT"]);
      this.setColour("#C93482");
      this.setTooltip('Declaración de una variable');
   }
};

Blockly.Blocks['one_more_local_variable'] = {
   init: function () {
      this.appendValueInput("INPUT").setCheck("OTHER_LOCAL_VARIABLE")
         .appendField(", ")
         .appendField(new Blockly.FieldTextInput("otraVariable"), "NAME");
      this.setOutput(true, "OTHER_LOCAL_VARIABLE");
      this.setColour("#C93482");
      this.setTooltip('Declaración de otra variable');
   }
};

Blockly.Blocks['declare_local_array'] = {
   init: function () {
      this.appendValueInput("INPUT").setCheck("OTHER_LOCAL_ARRAY")
         .appendField("lista de ")
         .appendField(new Blockly.FieldDropdown([["numero", "numero"], ["decimal", "decimal"], ["texto", "texto"], ["binario", "binario"]]), "TYPE")
         .appendField("de ")
         .appendField(new Blockly.FieldNumber(1, 1), "SIZE")
         .appendField(new Blockly.FieldTextInput("nombreLista"), "NAME");
      this.setPreviousStatement(true, "VARIABLE_LOCAL");
      this.setNextStatement(true, ["VARIABLE_LOCAL", "STATEMENT"]);
      this.setColour("#C93482");
      this.setTooltip('Declaración de una lista');
   }
};

Blockly.Blocks['one_more_local_array'] = {
   init: function () {
      this.appendValueInput("INPUT").setCheck("OTHER_LOCAL_ARRAY")
         .appendField(", ")
         .appendField(new Blockly.FieldTextInput("otraLista"), "NAME");
      this.setOutput(true, "OTHER_LOCAL_ARRAY");
      this.setColour("#C93482");
      this.setTooltip('Declaración de otra lista');
   }
};


// ********** Llamadas a funciones **********

Blockly.Blocks['call_function_without_params'] = {
   init: function () {
      this.appendDummyInput()
         .appendField(new Blockly.FieldTextInput("nombreFuncion"), "NAME");
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour("#EB509A");
   }
};

Blockly.Blocks['assign_call_function_without_params'] = {
   init: function () {
      this.appendDummyInput()
         .appendField(new Blockly.FieldTextInput("nombreFunción"), "NAME");
      this.setOutput(true, null);
      this.setColour("#EB509A");
   }
};

Blockly.Blocks['call_function_with_params'] = {
   init: function () {
      this.appendValueInput("PARAMETERS")
         .setCheck(null)
         .appendField(new Blockly.FieldTextInput("nombreFunción"), "NAME");
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour("#EB509A");
   }
};

Blockly.Blocks['assign_call_function_with_params'] = {
   init: function () {
      this.appendValueInput("PARAMETERS")
         .setCheck(null)
         .appendField(new Blockly.FieldTextInput("nombreFunción"), "NAME");
      this.setOutput(true, null);
      this.setColour("#EB509A");
   }
};

Blockly.Blocks['function_call_param'] = {
   init: function () {
      this.appendValueInput("PARAMETERS").setCheck("OTHER_PARAM_FUNCTION_CALL")
         .appendField(new Blockly.FieldTextInput("nombreParámetro"), "NAME");
      this.setOutput(true, "OTHER_PARAM_FUNCTION_CALL");
      this.setColour("#EB509A");
   }
};


// ********** Asignación **********

Blockly.Blocks['assignment'] = {
   init: function () {
      this.appendValueInput("INPUT").setCheck("EXPRESSION")
         .appendField(new Blockly.FieldTextInput("nombreVariable"), "NAME")
         .appendField(" = ");
      this.setPreviousStatement(true, "STATEMENT");
      this.setNextStatement(true, "STATEMENT");
      this.setColour("#00759A");
   }
};

Blockly.Blocks['value'] = {
   init: function () {
      this.appendDummyInput()
         .appendField(new Blockly.FieldTextInput("ValorOVariable"), "VALUE");
      this.setOutput(true, ['EXPRESSION', 'EXP'])
      this.setColour("#00759A");
   }
};


// ********** Expresión **********

Blockly.Blocks['expression_simple'] = {
   init: function () {
      this.appendValueInput("EXP1").setCheck("EXP");
      this.appendDummyInput();
      this.setOutput(true, ['EXP', 'EXPRESSION']);
      this.setColour("#0698BE");
   }
};

Blockly.Blocks['expression_compound'] = {
   init: function () {
      this.appendValueInput("EXP1").setCheck("EXP");
      this.appendDummyInput()
         .appendField(new Blockly.FieldDropdown([
            ["Mayor que", ">"],
            ["Menor que", "<"],
            ["Mayor o igual que", ">="],
            ["Menor o igual que", "<="],
            ["Igual a", "=="],
            ["Diferente a", "!="],
            ["+", "+"],
            ["-", "-"],
            ["*", "*"],
            ["/", "/"]
         ]), "TYPE");
      this.appendValueInput("EXP2").setCheck("EXP");
      this.appendDummyInput();
      this.setOutput(true, ['EXP', 'EXPRESSION']);
      this.setColour("#0698BE");
   }
};


// ********** Control de flujo **********

Blockly.Blocks['if'] = {
   init: function () {
      this.appendValueInput("CONTITION")
         .setCheck(null)
         .appendField("si sucede");
      this.appendStatementInput("ACTION")
         .setCheck(null)
         .appendField("realiza");
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, ['IF_ELSE', 'ELSE']);
      this.setColour("#5BCAE2");
   }
};

Blockly.Blocks['if_else'] = {
   init: function () {
      this.appendValueInput("CONTITION")
         .setCheck(null)
         .appendField("o si sucede");
      this.appendStatementInput("ACTION")
         .setCheck(null)
         .appendField("realiza");
      this.setPreviousStatement(true, 'IF_ELSE');
      this.setNextStatement(true, null);
      this.setColour("#5BCAE2");
   }
};

Blockly.Blocks['else'] = {
   init: function () {
      this.appendStatementInput("ACTION")
         .setCheck(null)
         .appendField("Si no sucede realiza");
      this.setPreviousStatement(true, 'ELSE');
      this.setNextStatement(true, null);
      this.setColour("#5BCAE2");
   }
};

Blockly.Blocks['while'] = {
   init: function () {
      this.appendValueInput("CONDITION")
         .setCheck(null)
         .appendField("Mientras sucede ");
      this.appendStatementInput("ACTION")
         .setCheck(null)
         .appendField("realiza");
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour("#66E2FC");
   }
};


// ********** Funciones predefinidas **********

Blockly.Blocks['read'] = {
   init: function () {
      this.appendDummyInput()
         .appendField("leer")
         .appendField(new Blockly.FieldTextInput("nombreVariable"), "VALUE");
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour("#0F2347");
   }
};

Blockly.Blocks['print'] = {
   init: function () {
      this.appendValueInput("PARAMETERS")
         .setCheck(null)
         .appendField("imprimir");
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour("#0F2347");
   }
};

Blockly.Blocks['add_to_list'] = {
   init: function () {
      this.appendDummyInput()
         .appendField("agregar a la lista:")
         .appendField(new Blockly.FieldTextInput("lista"), "LIST")
         .appendField("el valor:")
         .appendField(new Blockly.FieldTextInput("valor"), "VALUE")
         .appendField("en la posición:")
         .appendField(new Blockly.FieldTextInput("posición"), "POSITION");
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour("#0F2347");
   }
};

Blockly.Blocks['access_to_list'] = {
   init: function () {
      this.appendDummyInput()
         .appendField("acceder a la lista:")
         .appendField(new Blockly.FieldTextInput("lista"), "LIST")
         .appendField("en la posición:")
         .appendField(new Blockly.FieldTextInput("posición"), "POSITION");
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour("#0F2347");
   }
};

Blockly.Blocks['remove_last_to_list'] = {
   init: function () {
      this.appendDummyInput()
         .appendField("quitar ultimo de lista:")
         .appendField(new Blockly.FieldTextInput("lista"), "LIST")
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour("#0F2347");
   }
};

Blockly.Blocks['random'] = {
   init: function () {
      this.appendDummyInput()
         .appendField("número aleatorio con límite inferior:")
         .appendField(new Blockly.FieldTextInput("variableONumero"), "INF")
         .appendField("y límite superior:")
         .appendField(new Blockly.FieldTextInput("variableONumero"), "SUP");
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour("#0F2347");
   }
};


// ********** Comentarios **********

Blockly.Blocks['comment'] = {
   init: function () {
      this.appendDummyInput()
         .appendField("Comentario: ")
         .appendField(new Blockly.FieldTextInput("Mi comentario"), "VALUE");
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour("#17A92B");
   }
};

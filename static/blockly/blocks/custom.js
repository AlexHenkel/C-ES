goog.provide('Blockly.Blocks.custom');
goog.require('Blockly.Blocks');

// ********** Iniciar programa **********

Blockly.Blocks['programa'] = {
   init: function () {
      this.appendDummyInput().appendField("Programa");
      this.appendStatementInput("VAR_AND_FUNCS").setCheck(["VARIABLES", "FUNCTIONS"]);
      this.appendStatementInput("MAIN").setCheck("Main");
      this.setColour("#009494");
      this.setTooltip('Con este bloque se declara el inicio del programa');
   }
};


// ********** Declaración de variables **********

Blockly.Blocks['init_variables'] = {
   init: function () {
      this.appendDummyInput().appendField("Variables")
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
      this.setColour("#F35B05");
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
      this.setColour("#3A9C2D");
   }
};

Blockly.Blocks['function_param'] = {
   init: function () {
      this.appendValueInput("PARAMETERS").setCheck("OTHER_PARAM")
         .appendField(new Blockly.FieldDropdown([["numero", "numero"], ["decimal", "decimal"], ["texto", "texto"], ["binario", "binario"]]), "TYPE")
         .appendField(new Blockly.FieldTextInput("nombreParámetro"), "NAME");
      this.setOutput(true, "OTHER_PARAM");
      this.setColour("#F38C13");
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
      this.setColour("#3A9C2D");
   }
};

// ********** Declaración de variables locales **********

Blockly.Blocks['init_local_variables'] = {
   init: function () {
      this.appendDummyInput().appendField("Variables locales")
      this.setPreviousStatement(true, "LOCAL_VARIABLES");
      this.setNextStatement(true, ["VARIABLE_LOCAL", "STATEMENT"]);
      this.setColour("#F35B05");
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
      this.setColour("#F38C13");
      this.setTooltip('Declaración de una variable');
   }
};

Blockly.Blocks['one_more_local_variable'] = {
   init: function () {
      this.appendValueInput("INPUT").setCheck("OTHER_LOCAL_VARIABLE")
         .appendField(", ")
         .appendField(new Blockly.FieldTextInput("otraVariable"), "NAME");
      this.setOutput(true, "OTHER_LOCAL_VARIABLE");
      this.setColour("#F38C13");
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
      this.setColour("#F0B90C");
      this.setTooltip('Declaración de una lista');
   }
};

Blockly.Blocks['one_more_local_array'] = {
   init: function () {
      this.appendValueInput("INPUT").setCheck("OTHER_LOCAL_ARRAY")
         .appendField(", ")
         .appendField(new Blockly.FieldTextInput("otraLista"), "NAME");
      this.setOutput(true, "OTHER_LOCAL_ARRAY");
      this.setColour("#F0B90C");
      this.setTooltip('Declaración de otra lista');
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
      this.setColour("#F38C13");
   }
};

Blockly.Blocks['value'] = {
   init: function () {
      this.appendDummyInput()
         .appendField(new Blockly.FieldTextInput("Valor"), "VALOR");
      this.setOutput(true, ['EXPRESSION', 'EXP'])
      this.setColour("#FFDE00");
   }
};


// ********** Expresión **********

Blockly.Blocks['expression_simple'] = {
   init: function () {
      this.appendValueInput("EXP1").setCheck("EXP");
      this.appendDummyInput();
      this.setOutput(true, ['EXP', 'EXPRESSION']);
      this.setColour("#E183E8");
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
      this.setColour("#E183E8");
   }
};
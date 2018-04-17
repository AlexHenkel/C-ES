'use strict';
goog.provide('Blockly.Blocks.custom');
goog.require('Blockly.Blocks');

// ********** Iniciar programa **********

Blockly.Blocks['programa'] = {
   init: function () {
      this.appendDummyInput().appendField("Programa");
      this.appendStatementInput("VAR_AND_FUNCS").setCheck(["Variables", "Functions"]);
      this.appendStatementInput("MAIN").setCheck("Main");
      this.setColour("#009494");
      this.setTooltip('Aquí se declara el inicio del programa');
   }
};


// ********** Declaración de variables **********

Blockly.Blocks['init_variables'] = {
   init: function () {
      this.appendDummyInput().appendField("Variables")
      this.setPreviousStatement(true, "Variables");
      this.setNextStatement(true, "Variable");
      this.setColour("#F35B05");
      this.setTooltip('Aquí se declaran las variables globales');
   }
};

Blockly.Blocks['declare_variable'] = {
   init: function () {
      this.appendValueInput("INPUT").setCheck("otraVariable")
      .appendField(new Blockly.FieldDropdown([["numero", "numero"], ["decimal", "decimal"], ["texto", "texto"], ["binario", "binario"]]), "TYPE")
      .appendField(new Blockly.FieldTextInput("nombreVariable"), "NAME");
      this.setPreviousStatement(true, "Variable");
      this.setNextStatement(true, "Variable");
      this.setColour("#F38C13");
      this.setTooltip('Aquí se declara una variable');
   }
};

Blockly.Blocks['one_more_variable'] = {
   init: function () {
      this.appendValueInput("INPUT").setCheck("otraVariable")
         .appendField(", ")
         .appendField(new Blockly.FieldTextInput("otraVariable"), "NAME");
      this.setOutput(true, "otraVariable");
      this.setColour("#F38C13");
      this.setTooltip('Aquí se declara otra variable');
   }
};

Blockly.Blocks['declare_array'] = {
   init: function () {
      this.appendValueInput("INPUT").setCheck("otroArreglo")
         .appendField("lista de ")
         .appendField(new Blockly.FieldDropdown([["numero", "numero"], ["decimal", "decimal"], ["texto", "texto"], ["binario", "binario"]]), "TYPE")
         .appendField("de ")
         .appendField(new Blockly.FieldNumber(1, 1), "SIZE")
         .appendField(new Blockly.FieldTextInput("nombreArreglo"), "NAME");
      this.setPreviousStatement(true, "Variable");
      this.setNextStatement(true, "Variable");
      this.setColour("#F0B90C");
      this.setTooltip('Aquí se declara un arreglo');
   }
};

Blockly.Blocks['one_more_array'] = {
   init: function () {
      this.appendValueInput("INPUT").setCheck("otroArreglo")
         .appendField(", ")
         .appendField(new Blockly.FieldTextInput("otroArreglo"), "NAME");
      this.setOutput(true, "otroArreglo");
      this.setColour("#F0B90C");
      this.setTooltip('Aquí se declara otra variable');
   }
};
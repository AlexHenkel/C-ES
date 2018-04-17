// ********** Iniciar programa **********

Blockly.JavaScript['programa'] = function (block) {
   var variablesAndFuntions = Blockly.JavaScript.statementToCode(block, 'VAR_AND_FUNCS');
   var main = Blockly.JavaScript.statementToCode(block, 'MAIN');
   var code = '';

   if (variablesAndFuntions === "") {
      code = '  programa\n\n{\n' + main + '\n  }';
   } else {
      code = '  programa\n\n' + variablesAndFuntions + '\n  {\n' + main + '\n  }';
   }
   return code;
};


// ********** Declaración de variables **********

Blockly.JavaScript['init_variables'] = function (block) {
   var variables = Blockly.JavaScript.statementToCode(block, 'VARIABLES');
   var code = 'variables: \n' + variables;
   return code;
};

Blockly.JavaScript['declare_variable'] = function (block) {
   var type = block.getFieldValue('TYPE');
   var name = block.getFieldValue('NAME');
   var inputs = Blockly.JavaScript.statementToCode(block, 'INPUT').trim();
   var code = '';
   console.log('declare_variable', inputs, name, type);

   if (inputs != "") {
      code = type + ' ' + name + ', ' + inputs + ';\n';
   } else {
      code = type + ' ' + name + ';\n';
   }
   return code;
};

Blockly.JavaScript['one_more_variable'] = function (block) {
   var name = block.getFieldValue('NAME');
   var inputs = Blockly.JavaScript.statementToCode(block, 'INPUT').trim();
   var code = '';
   console.log('one_more_variable', inputs, name);

   if (inputs != "") {
      code = name + ', ' + inputs;
   } else {
      code = name;
   }

   code.trim()
   return code;
};

Blockly.JavaScript['declare_array'] = function (block) {
   var type = block.getFieldValue('TYPE');
   var name = block.getFieldValue('NAME');
   var size = block.getFieldValue('SIZE');
   var inputs = Blockly.JavaScript.statementToCode(block, 'INPUT').trim();
   var code = '';
   console.log('declare_array', inputs, name, type, size);

   if (inputs != "") {
      code = 'lista de ' + type + ' de ' + size + ' ' + name + ', ' + inputs + ';\n';
   } else {
      code = 'lista de ' + type + ' de ' + size + ' ' + name + ';\n';
   }

   return code;
};

Blockly.JavaScript['one_more_array'] = function (block) {
   var name = block.getFieldValue('NAME');
   var inputs = Blockly.JavaScript.statementToCode(block, 'INPUT').trim();
   var code = '';
   console.log('one_more_array', inputs, name);

   if (inputs != "") {
      code = name + ', ' + inputs;
   } else {
      code = name;
   }
   return code;
};


// ********** Declaración de funciones **********

Blockly.JavaScript['function_with_params'] = function (block) {
   var name = block.getFieldValue('NAME');
   var type = block.getFieldValue('TYPE');
   var inputs = Blockly.JavaScript.statementToCode(block, 'PARAMETERS').trim();
   var body = Blockly.JavaScript.statementToCode(block, 'BODY_FUNCTION');
   var code = '';
   console.log('function_with_params', inputs, name, type);

   if (inputs === "") {
      console.log('empty');
      if (type === "nada") {
         code = "funcion " + name + "() {\n" + body + "\n}";
      } else {
         code = type + " funcion " + name + "() {\n" + body + "\n}";
      }
   } else {
      console.log('no empty');
      if (type === "nada") {
         code = "funcion " + name + "(" + inputs + ") {\n" + body + "\n}";
      } else {
         code = type + " funcion " + name + "(" + inputs + ") {\n" + body + "\n}";
      }
   }
   return code;
};

Blockly.JavaScript['function_param'] = function (block) {
   var name = block.getFieldValue('NAME');
   var type = block.getFieldValue('TYPE');
   var inputs = Blockly.JavaScript.statementToCode(block, "PARAMETERS").trim();
   var code = '';
   console.log('function_param', inputs, name, type);

   if (inputs !== "") {
      console.log('inputssss');
      code = type + ' ' + name + ', ' + inputs;
   } else {
      console.log('NO inputssss');
      code = type + ' ' + name;
   }

   return code;
};

Blockly.JavaScript['function_without_params'] = function (block) {
   var name = block.getFieldValue('NAME');
   var type = block.getFieldValue('TYPE');
   var body = Blockly.JavaScript.statementToCode(block, 'BODY_FUNCTION');
   var code = '';
   console.log('function_without_params', name, type);

   if (type === "nada") {
      code = "funcion " + name + "() {\n" + body + "\n}";
   } else {
      code = type + " funcion " + name + "() {\n" + body + "\n}";
   }

   return code;
};
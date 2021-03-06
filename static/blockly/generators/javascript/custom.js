// ********** Iniciar programa **********

Blockly.JavaScript['programa'] = function (block) {
   var variablesAndFuntions = Blockly.JavaScript.statementToCode(block, 'VAR_AND_FUNCS');
   var main = Blockly.JavaScript.statementToCode(block, 'MAIN');
   var code = '';

   if (variablesAndFuntions === "") {
      code = '<span class="reserved-word">programa</span>\n\n{\n' + main + '}';
   } else {
      console.log('programa variablesAndFuntions', variablesAndFuntions);
      code = '<span class="reserved-word">programa</span>\n' + variablesAndFuntions + '\n{\n' + main + '}';
   }

   return code;
};


// ********** Declaración de variables **********

Blockly.JavaScript['init_variables'] = function (block) {
   console.log('init_variables');
   var variables = Blockly.JavaScript.statementToCode(block, 'VARIABLES');
   var code = '\n<span class="reserved-word-2">variables:</span>\n';
   
   if (!block.nextConnection.targetConnection) {
      code = '';
   } else if (block.nextConnection.targetConnection.check_.length === 2) {
      code = '';
   }

   return code;
};

Blockly.JavaScript['declare_variable'] = function (block) {
   var type = '<span class="reserved-word-3">' + block.getFieldValue('TYPE') + '</span>';
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

   return code;
};

Blockly.JavaScript['declare_array'] = function (block) {
   var type = '<span class="reserved-word-3">' + block.getFieldValue('TYPE') + '</span>';
   var name = block.getFieldValue('NAME');
   var size = block.getFieldValue('SIZE');
   var inputs = Blockly.JavaScript.statementToCode(block, 'INPUT').trim();
   var code = '';
   console.log('declare_array', inputs, name, type, size);

   if (inputs != "") {
      code = '<span class="reserved-word-3">lista</span> de ' + type + ' de ' + size + ' ' + name + ', ' + inputs + ';\n';
   } else {
      code = '<span class="reserved-word-3">lista</span> de ' + type + ' de ' + size + ' ' + name + ';\n';
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

Blockly.JavaScript['init_functions'] = function (block) {
   console.log('init_functions');
   var variables = Blockly.JavaScript.statementToCode(block, 'VARIABLES');
   var code = '\n<span class="reserved-word-2">funciones:</span>\n';

   if (!block.nextConnection.targetConnection) {
      code = '';
   } else if (block.nextConnection.targetConnection.check_.length === 2) {
      code = '';
   }

   return code;
}

Blockly.JavaScript['function_with_params'] = function (block) {
   var name = block.getFieldValue('NAME');
   var type = block.getFieldValue('TYPE');
   var inputs = Blockly.JavaScript.statementToCode(block, 'PARAMETERS').trim();
   var body = Blockly.JavaScript.statementToCode(block, 'BODY_FUNCTION');
   var code = '';
   console.log('function_with_params', inputs, name, type);
   console.log(block);
   if (inputs === "") {
      console.log('empty');
      if (type === "nada") {
         code = "<span class='reserved-word-3'>funcion</span> " + name + "() {\n" + body + "\n}\n";
      } else {
         code = "<span class='reserved-word-3'>" + type + "</span>" + " <span class='reserved-word-3'>funcion</span> " + name + "() {\n" + body + "\n}\n";
      }
   } else {
      console.log('no empty');
      if (type === "nada") {
         code = "<span class='reserved-word-3'>funcion</span> " + name + "(" + inputs + ") {\n" + body + "\n}\n";
      } else {
         code = "<span class='reserved-word-3'>" + type + "</span>" + " <span class='reserved-word-3'>funcion</span> " + name + "(" + inputs + ") {\n" + body + "}\n";
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
      code = "<span class='reserved-word-3'>" + type + "</span>" + ' ' + name + ', ' + inputs;
   } else {
      console.log('NO inputssss');
      code = "<span class='reserved-word-3'>" + type + "</span>" + ' ' + name;
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
      code = "<span class='reserved-word-3'>funcion</span> " + name + "() {\n" + body + "\n}\n";
   } else {
      code = "<span class='reserved-word-3'>" + type + "</span>" + " <span class='reserved-word-3'>funcion</span> " + name + "() {\n" + body + "}\n";
   }

   return code;
};

Blockly.JavaScript['return'] = function (block) {
   var returnInput = Blockly.JavaScript.statementToCode(block, 'RETURN').trim();
   var code = '<span class="reserved-word-3">devolver</span> ' + returnInput + '\n';
   return code;
};


// ********** Declaración de variables locales **********

Blockly.JavaScript['init_local_variables'] = function (block) {
   console.log('init_local_variables');
   var variables = Blockly.JavaScript.statementToCode(block, 'VARIABLES');
   var code = '<span class="reserved-word-2">variables:</span>\n';

   if (!block.nextConnection.targetConnection) {
      code = '';
   } else if (block.nextConnection.targetConnection.check_.length === 2) {
      code = '';
   }
   console.log(block.nextConnection.targetConnection);

   return code;
};

Blockly.JavaScript['declare_local_variable'] = function (block) {
   var type = block.getFieldValue('TYPE');
   var name = block.getFieldValue('NAME');
   var inputs = Blockly.JavaScript.statementToCode(block, 'INPUT').trim();
   var code = '';
   console.log('declare_local_variable', inputs, name, type);

   if (inputs != "") {
      code = "<span class='reserved-word-3'>" + type + "</span>" + ' ' + name + ', ' + inputs + ';\n';
   } else {
      code = "<span class='reserved-word-3'>" + type + "</span>" + ' ' + name + ';\n';
   }
   return code;
};

Blockly.JavaScript['one_more_local_variable'] = function (block) {
   var name = block.getFieldValue('NAME');
   var inputs = Blockly.JavaScript.statementToCode(block, 'INPUT').trim();
   var code = '';
   console.log('one_more_local_variable', inputs, name);

   if (inputs != "") {
      code = name + ', ' + inputs;
   } else {
      code = name;
   }

   return code;
};

Blockly.JavaScript['declare_local_array'] = function (block) {
   var type = block.getFieldValue('TYPE');
   var name = block.getFieldValue('NAME');
   var size = block.getFieldValue('SIZE');
   var inputs = Blockly.JavaScript.statementToCode(block, 'INPUT').trim();
   var code = '';
   console.log('declare_local_array', inputs, name, type, size);

   if (inputs != "") {
      code = '<span class="reserved-word-3">lista</span> de ' + "<span class='reserved-word-3'>" + type + "</span>" + ' de ' + size + ' ' + name + ', ' + inputs + ';\n';
   } else {
      code = '<span class="reserved-word-3">lista</span> de ' + "<span class='reserved-word-3'>" + type + "</span>" + ' de ' + size + ' ' + name + ';\n';
   }

   return code;
};

Blockly.JavaScript['one_more_local_array'] = function (block) {
   var name = block.getFieldValue('NAME');
   var inputs = Blockly.JavaScript.statementToCode(block, 'INPUT').trim();
   var code = '';
   console.log('one_more_local_array', inputs, name);

   if (inputs != "") {
      code = name + ', ' + inputs;
   } else {
      code = name;
   }
   return code;
};


// ********** Llamadas a funciones **********

Blockly.JavaScript['call_function_without_params'] = function (block) {
   var name = block.getFieldValue('NAME');
   return name + '()\n';
}

Blockly.JavaScript['assign_call_function_without_params'] = function (block) {
   var name = block.getFieldValue('NAME');
   console.log('assign_call_function_without_params', name);
   return name + '()\n';
};

Blockly.JavaScript['call_function_with_params'] = function (block) {
   var name = block.getFieldValue('NAME');
   var params = Blockly.JavaScript.statementToCode(block, 'PARAMETERS').trim();
   var code = name + '(' + params + ')\n';
   return code;
};


Blockly.JavaScript['assign_call_function_with_params'] = function (block) {
   var name = block.getFieldValue('NAME');
   var params = Blockly.JavaScript.statementToCode(block, 'PARAMETERS').trim();
   var code = name + '(' + params + ')\n';
   return code;
};

Blockly.JavaScript['function_call_param'] = function (block) {
   var name = block.getFieldValue('NAME');
   var inputs = Blockly.JavaScript.statementToCode(block, "PARAMETERS").trim();
   var code = '';
   console.log('function_call_param', inputs, name);

   if (inputs !== "") {
      console.log('inputssss');
      code = name + ', ' + inputs;
   } else {
      console.log('NO inputssss');
      code = name;
   }

   return code;
};


// ********** Asignación **********

Blockly.JavaScript['assignment'] = function (block) {
   var name = block.getFieldValue('NAME');
   var inputs = Blockly.JavaScript.statementToCode(block, 'INPUT').trim();
   return name + ' = ' + inputs + '\n';
}

Blockly.JavaScript['value'] = function (block) {
   var value = block.getFieldValue('VALUE');
   console.log('value', value);
   return value;
}


// ********** Expresión **********

Blockly.JavaScript['expression_simple'] = function (block) {
   var inputs = Blockly.JavaScript.statementToCode(block, 'EXP1').trim();
   console.log('expression_simple', inputs);
   code = '';

   if (inputs != "") {
      code = inputs
   } 
   
   return code;
}

Blockly.JavaScript['expression_compound'] = function (block) {
   var inputsLeft = Blockly.JavaScript.statementToCode(block, 'EXP1').trim();
   var inputsRight = Blockly.JavaScript.statementToCode(block, 'EXP2').trim();
   var type = block.getFieldValue('TYPE');
   console.log('expression_compound', inputsLeft, inputsRight, type);

   return inputsLeft + ' ' + type + ' ' + inputsRight;
}


// ********** Control de flujo **********

Blockly.JavaScript['if'] = function (block) {
   var condition = Blockly.JavaScript.statementToCode(block, 'CONTITION').trim();
   var action = Blockly.JavaScript.statementToCode(block, 'ACTION');
   console.log('if', condition, action);

   var code = '<span class="reserved-word">si sucede</span> (' + condition + ') <span class="reserved-word">realiza</span> {\n' + action + '\n}\n';
   return code;
};

Blockly.JavaScript['if_else'] = function (block) {
   var condition = Blockly.JavaScript.statementToCode(block, 'CONTITION').trim();
   var action = Blockly.JavaScript.statementToCode(block, 'ACTION');
   console.log('if', condition, action);

   var code = '<span class="reserved-word">o si sucede</span> (' + condition + ') <span class="reserved-word">realiza</span> {\n' + action + '\n}\n';
   return code;
};

Blockly.JavaScript['else'] = function (block) {
   var accion = Blockly.JavaScript.statementToCode(block, 'ACTION');
   var code = '<span class="reserved-word">no sucede</span> ' + '{\n' + accion + '\n}\n';
   return code;
};

Blockly.JavaScript['while'] = function (block) {
   var condicion = Blockly.JavaScript.statementToCode(block, 'CONDITION').trim();
   var accion = Blockly.JavaScript.statementToCode(block, 'ACTION');
   var code = '<span class="reserved-word">mientras sucede</span> (' + condicion + ') <span class="reserved-word">realiza</span> { \n' + accion + '}\n';
   return code;
};


// ********** Funciones predefinidas **********

Blockly.JavaScript['read'] = function (block) {
   var value = block.getFieldValue('VALUE');
   var code = '<span class="reserved-word">leer</span>(' + value + ')\n';
   return code;
};

Blockly.JavaScript['print'] = function (block) {
   var params = Blockly.JavaScript.statementToCode(block, 'PARAMETERS').trim();
   var code = '<span class="reserved-word">imprimir</span>(' + params + ')\n';
   return code;
};

Blockly.JavaScript['add_to_list'] = function (block) {
   var list = block.getFieldValue('LIST');
   var value = block.getFieldValue('VALUE');
   var position = block.getFieldValue('POSITION');
   var code = '<span class="reserved-word">agregar a</span>(' + list + ', ' + value + ', ' + position + ')\n';
   return code;
};

Blockly.JavaScript['access_to_list'] = function (block) {
   var list = block.getFieldValue('LIST');
   var position = block.getFieldValue('POSITION');
   var code = '<span class="reserved-word">acceder</span>(' + list + ', ' + position + ')\n';
   return code;
};

Blockly.JavaScript['remove_last_to_list'] = function (block) {
   var list = block.getFieldValue('LIST');
   var code = '<span class="reserved-word">quitar ultimo de</span> ' + list + '()\n';
   return code;
};

Blockly.JavaScript['random'] = function (block) {
   var inf = block.getFieldValue('INF');
   var sup = block.getFieldValue('SUP');
   var code = '<span class="reserved-word">numero aleatorio</span>(' + inf + ', ' + sup + ')\n';
   return code;
};


// ********** Comentarios **********

Blockly.JavaScript['comment'] = function (block) {
   var value = block.getFieldValue('VALUE');
   var code = '<span class="comment">// ' + value + '</span>\n';
   return code;
};
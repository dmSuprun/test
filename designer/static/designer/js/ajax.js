 function mapToObj(map){
                  const obj = {}
                  for (let [k,v] of map)
                    obj[k] = v
                  return obj
                }


            if (ValidError === false){
                var requestToServ = new Map();
                requestToServ.set('questions', mapToObj(questions))
                requestToServ.set('functions', mapToObj(functions))
                requestToServ.set('inputArg', mapToObj(inputArguments))
                requestToServ.set('outputArg',mapToObj(outputArgs))

                const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;


                var xhr = new XMLHttpRequest();
                xhr.open('POST','http://127.0.0.1:8000/create/{{test}}/task/')
                xhr.setRequestHeader('Content-Type', 'application/json' );
                xhr.setRequestHeader('X-CSRFToken',  csrftoken );
                //const obj =Object.fromEntries(requestToServ);
                xhr.send(JSON.stringify(mapToObj(requestToServ)))

            }
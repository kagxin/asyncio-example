# Asyncio Finite State Machine
import asyncio
import time
from random import randint


async def StartState():
    print("Start State called \n")
    # input_value = randint(0, 1)
    input_value = 1
    time.sleep(1)
    if input_value == 0:
        result = await State2(input_value)
    else:
        result = await State1(input_value)
    print("Resume of the Transition : \nStart State calling " + result)


async def State1(transition_value):
    outputValue = str("State 1 with transition value = %s \n" % transition_value)
    input_value = randint(0, 1)
    input_value = 1
    time.sleep(1)
    print("...Evaluating...")
    if input_value == 0:
        result = await State3(input_value)
    else:
        result = await State2(input_value)
    result = "State 1 calling " + result
    print('+1')
    return outputValue + str(result)


async def State2(transition_value):
    outputValue = str("State 2 with transition value = %s \n" % transition_value)
    input_value = randint(0, 1)
    input_value = 1
    time.sleep(1)
    print("...Evaluating...")
    if input_value == 0:
        result = await State1(input_value)
    else:
        result = await State3(input_value)
    result = "State 2 calling " + result
    print('+2')
    return outputValue + str(result)


async def State3(transition_value):
    outputValue = str("State 3 with transition value = %s \n" % transition_value)
    input_value = randint(0, 1)
    input_value = 1
    time.sleep(1)
    print("...Evaluating...")
    if input_value == 0:
        result = await State1(input_value)
    else:
        result = await EndState(input_value)
    result = "State 3 calling " + result
    print('+3')
    return outputValue + str(result)


async def EndState(transition_value):
    outputValue = str("End State with transition value = %s \n" % transition_value)
    print("...Stop Computation...")
    await asyncio.sleep(5)
    return outputValue


if __name__ == "__main__":
    print("Finite State Machine simulation with Asyncio Coroutine")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(StartState())


"""
await   挂起协程
return  终止调用栈，返回await "等待" 的值
"""
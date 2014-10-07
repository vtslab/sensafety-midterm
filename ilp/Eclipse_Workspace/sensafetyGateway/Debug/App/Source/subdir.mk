################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../App/Source/main.c 

OBJS += \
./App/Source/main.o 

C_DEPS += \
./App/Source/main.d 


# Each subdirectory must supply rules for building sources it contributes
App/Source/%.o: ../App/Source/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: Cross GCC Compiler'
	arm-linux-gnueabihf-gcc -I/home/jeffrey/software/mqtt-lib/include -I"/home/jeffrey/software/workspace/sensafetyGateway" -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '



################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../App/Source/LampDriver/LampDriver.c 

OBJS += \
./App/Source/LampDriver/LampDriver.o 

C_DEPS += \
./App/Source/LampDriver/LampDriver.d 


# Each subdirectory must supply rules for building sources it contributes
App/Source/LampDriver/%.o: ../App/Source/LampDriver/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: Cross GCC Compiler'
	arm-linux-gnueabihf-gcc -I/home/jeffrey/software/mqtt-lib/include -I"/home/jeffrey/software/workspace/sensafetyGateway" -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '



################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../App/Source/SapDriver/SapDriver.c 

OBJS += \
./App/Source/SapDriver/SapDriver.o 

C_DEPS += \
./App/Source/SapDriver/SapDriver.d 


# Each subdirectory must supply rules for building sources it contributes
App/Source/SapDriver/%.o: ../App/Source/SapDriver/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: Cross GCC Compiler'
	arm-linux-gnueabihf-gcc -I/home/jeffrey/software/mqtt-lib/include -I"/home/jeffrey/software/workspace/sensafetyGateway" -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '



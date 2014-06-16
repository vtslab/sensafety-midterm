################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Bsp/Source/Bsp_GPIO/gpio_e.c 

OBJS += \
./Bsp/Source/Bsp_GPIO/gpio_e.o 

C_DEPS += \
./Bsp/Source/Bsp_GPIO/gpio_e.d 


# Each subdirectory must supply rules for building sources it contributes
Bsp/Source/Bsp_GPIO/%.o: ../Bsp/Source/Bsp_GPIO/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: Cross GCC Compiler'
	arm-unknown-linux-gnueabi-gcc -std=c99 -I"c:\cygwin\opt\cross\x-tools\arm-unknown-linux-gnueabi\arm-unknown-linux-gnueabi\sysroot\usr\include" -I"/home/jeffrey/projects/MidTerm/ilp/Eclipse_Workspace/toggle_led_threads" -O0 -g3 -Wall -c -fmessage-length=0 -pthread -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '



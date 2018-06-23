	BITS 16

start:
	LF	equ	10
	CR	equ	13

	mov ax, 07C0h		; Set up 4K stack space after this bootloader
	add ax, 288		; (4096 + 512) / 16 bytes per paragraph
	mov ss, ax
	mov sp, 4096

	mov ax, 07C0h		; Set data segment to where we're loaded
	mov ds, ax


	mov	bl, 1 ;BL is used as color attribute
	mov ah,0
	mov al,03h	;25*80
	int 10h

	mov	si, welcome
	call print_string
	mov	si, text_string
	call print_string

Menu:

	;mov	dh, 2
	;mov	dl, 0

;	mov	ah, 08h
;	int	10h

	mov ah,00h
	int 16h  ; gets char
	mov	ah,0Eh
	int 10h ; prints the char

	; Compare to 1 : Print about me
	cmp al, '1'
	jne	next1
	mov si, about_me	; Put string position into SI
	call print_string	; Call our string-printing routine
	mov	si, text_string
	call print_string
	next1:

	; prints menu
	cmp al, '2'
	jne	next2
	mov	si, newLine
	call print_string
	mov	si, text_string
	call print_string
	;hlt
	next2:

	; Clears the screen
	cmp	al, '3'
	jne	next3
	call clear
	mov	si, text_string
	call print_string
	next3:

	; restarts the OS
	cmp	al, '4'
	jne	next4
	call restart
	next4:

	;jmp $			; Jump here - infinite loop!
	jmp	Menu


	;color		db	1
	newLine		db CR, LF, 0
	welcome		db '{._.} Welcome to Arashs Unique Useless '
				db 'Operating System ( AUUOS )', CR, LF
				db '/[.]\', CR, LF
				db '[] []', CR, LF, 0
	text_string	db CR, LF
				db '1) About Me',CR,LF
				db '2) Print menu', CR, LF
				db '3) Clear screen and change color',CR,LF
				db '4) Restarts the OS (!!!) : ', 0

	about_me	db CR, LF, CR, LF
				db 13, 10, 'Arash Taher '
				db 'Shiraz university'
				db ' (882980) ', 13, 10
				db 'This the first OS that has been '
				db 'written by me', 13, 10
				db 'My email : '
				db 'arashTaherK at gmail (dot) com'
				db 13, 10, 13, 10, 0

print_string:			; Routine: output string in SI to screen
	mov ah, 0Eh		; int 10h 'print char' function

.repeat:
	lodsb			; Get character from string
	cmp al, 0
	je .done		; If char is zero, end of string
	int 10h			; Otherwise, print it
	jmp .repeat

.done:
	ret

aboutMe:
	mov	si, about_me
	call print_string
	ret

clear:
	cmp	bl, 0Fh ; BL is used as color attribute
	je setAgain
	inc	bl
	jmp	goOn
	setAgain:
	mov	bl, 1
	goOn:
	mov	ah, 07h
	mov	al, 00h
	mov ch,0
	mov cl,0
	mov dh,25
	mov dl,80
	mov	bh, bl
	int 10h
	; set cursor position
	mov	ah, 02h
	mov	bh, 0
	mov	dh, 0
	mov	dl, 0
	int 10h
	ret

restart:
	db	0xEA	; Far jump to ...
	dw	0x0000	; 0000:
	dw	0xFFFF	; FFFF
	ret

	times 510-($-$$) db 0	; Pad remainder of boot sector with 0s
	dw 0xAA55		; The standard PC boot signature

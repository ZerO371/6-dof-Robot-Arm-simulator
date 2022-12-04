import numpy as np
from numpy import sin, cos
import matplotlib
# matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import mpl_toolkits.mplot3d.axes3d as ax3d
import matplotlib.animation as animation
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk


N = 60
# DH parameters
d_1, d_2, d_3, d_4, d_5 = 0, 0, 0, 0, 0
l_1, l_2, l_3, l_4, l_5 = -0.2, 1, 1, 1, 1
alpha_1, alpha_2, alpha_3, alpha_4, alpha_5 = 90, 0, 0, 0, 0
theta1_0, theta1_1 = 90, 90
theta2_0, theta2_1 = 45, 45
theta3_0, theta3_1 = 45, 45
theta4_0, theta4_1 = 45, 45
theta5_0, theta5_1 = 45, 45
# x,y,z coordinates
x, y, z = np.array([]), np.array([]), np.array([])
anime_array = np.array([])
ani_is_finished = False


# DH matrix
def DH_method(delta, d, a, alpha):
    return np.array([[cos(delta), -sin(delta) * cos(alpha), sin(delta) * sin(alpha), a * cos(delta)],
                     [sin(delta), cos(delta) * cos(alpha), -cos(delta) * sin(alpha), a * sin(delta)],
                     [0, sin(alpha), cos(alpha), d],
                     [0, 0, 0, 1]])


# dot product
def DH_calculation():
    global x, y, z, anime_array
    list_pos = []
    theta_1 = np.radians(np.linspace(theta1_0, theta1_1, N))
    theta_2 = np.radians(np.linspace(theta2_0, theta2_1, N))
    theta_3 = np.radians(np.linspace(theta3_0, theta3_1, N))
    theta_4 = np.radians(np.linspace(theta4_0, theta4_1, N))
    theta_5 = np.radians(np.linspace(theta5_0, theta5_1, N))

    P_0 = np.array([0, 0, 0, 1]).T
    P_1 = np.array([0, 0, 0, 1]).T
    P_2 = np.array([0, 0, 0, 1]).T
    P_3 = np.array([0, 0, 0, 1]).T
    P_4 = np.array([0, 0, 0, 1]).T
    P_5 = np.array([0, 0, 0, 1]).T

    # Calculate each end coordinate in loop
    for i in range(len(theta_1)):
        P1_0 = DH_method(theta_1[i], d_1, l_1, alpha_1).dot(P_1)
        P2_0 = (DH_method(theta_1[i], d_1, l_1, alpha_1).dot(DH_method(theta_2[i], d_2, l_2, alpha_2)).dot(P_2))
        P3_0 = (DH_method(theta_1[i], d_1, l_1, alpha_1).dot(DH_method(theta_2[i], d_2, l_2, alpha_2))
                .dot(DH_method(theta_3[i], d_3, l_3, alpha_3)).dot(P_3))
        P4_0 = (DH_method(theta_1[i], d_1, l_1, alpha_1).dot(DH_method(theta_2[i], d_2, l_2, alpha_2))
                .dot(DH_method(theta_3[i], d_3, l_3, alpha_3)).dot(DH_method(theta_4[i], d_4, l_4, alpha_4))).dot(P_4)
        P5_0 = (DH_method(theta_1[i], d_1, l_1, alpha_1).dot(DH_method(theta_2[i], d_2, l_2, alpha_2))
                .dot(DH_method(theta_3[i], d_3, l_3, alpha_3)).dot(DH_method(theta_4[i], d_4, l_4, alpha_4))
                .dot(DH_method(theta_5[i], d_5, l_5, alpha_5)).dot(P_5))
        list_pos.append([[P_0[2], P1_0[2], P2_0[2], P3_0[2], P4_0[2], P5_0[2]]
                               , [P_0[1], P1_0[1], P2_0[1], P3_0[1], P4_0[1], P5_0[1]]
                               , [P_0[0], P1_0[0], P2_0[0], P3_0[0], P4_0[0], P5_0[0]]])
        # ax.plot([P_0[2], P1_0[2], P2_0[2], P3_0[2], P4_0[2], P5_0[2]]
        #        , [P_0[1], P1_0[1], P2_0[1], P3_0[1], P4_0[1], P5_0[1]]
        #        , [P_0[0], P1_0[0], P2_0[0], P3_0[0], P4_0[0], P5_0[0]], 'o-m')
    # xyz anime list
    anime_array = np.array(list_pos)
    x = anime_array[:N, 0, :6]
    y = anime_array[:N, 1, :6]
    z = anime_array[:N, 2, :6]


# Calculate each end coordinate each time
def DH_calculation_list(list_theta, list_d, list_l, list_alpha):
    global x, y, z, anime_array
    list_pos = []
    theta_1 = np.radians(np.linspace(list_theta[0], list_theta[1], N))
    theta_2 = np.radians(np.linspace(list_theta[2], list_theta[3], N))
    theta_3 = np.radians(np.linspace(list_theta[4], list_theta[5], N))
    theta_4 = np.radians(np.linspace(list_theta[6], list_theta[7], N))
    theta_5 = np.radians(np.linspace(list_theta[8], list_theta[9], N))

    P_0 = np.array([0, 0, 0, 1]).T

    for i in range(len(theta_1)):
        P1_0 = DH_method(theta_1[i], list_d[0], list_l[0], list_alpha[0]).dot(P_0)
        P2_0 = (DH_method(theta_1[i], list_d[0], list_l[0], list_alpha[0])
                .dot(DH_method(theta_2[i], list_d[1], list_l[1], list_alpha[1])).dot(P_0))
        P3_0 = (DH_method(theta_1[i], list_d[0], list_l[0], list_alpha[0])
                .dot(DH_method(theta_2[i], list_d[1], list_l[1], list_alpha[1]))
                .dot(DH_method(theta_3[i], list_d[2], list_l[2], list_alpha[2])).dot(P_0))
        P4_0 = (DH_method(theta_1[i], list_d[0], list_l[0], list_alpha[0])
                .dot(DH_method(theta_2[i], list_d[1], list_l[1], list_alpha[1]))
                .dot(DH_method(theta_3[i], list_d[2], list_l[2], list_alpha[2]))
                .dot(DH_method(theta_4[i], list_d[3], list_l[3], list_alpha[3]))).dot(P_0)
        P5_0 = (DH_method(theta_1[i], list_d[0], list_l[0], list_alpha[0])
                .dot(DH_method(theta_2[i], list_d[1], list_l[1], list_alpha[1]))
                .dot(DH_method(theta_3[i], list_d[2], list_l[2], list_alpha[2]))
                .dot(DH_method(theta_4[i], list_d[3], list_l[3], list_alpha[3]))
                .dot(DH_method(theta_5[i], list_d[4], list_l[4], list_alpha[4])).dot(P_0))
        list_pos.append([[P_0[0], P1_0[0], P2_0[0], P3_0[0], P4_0[0], P5_0[0]]
                        , [P_0[1], P1_0[1], P2_0[1], P3_0[1], P4_0[1], P5_0[1]]
                        , [P_0[2], P1_0[2], P2_0[2], P3_0[2], P4_0[2], P5_0[2]]])
    anime_array = np.array(list_pos)
    x = anime_array[:N, 0, :6]
    y = anime_array[:N, 1, :6]
    z = anime_array[:N, 2, :6]


def main():
    global x, y, z, anime_array, ani_is_finished
    root = tk.Tk()
    root.title("DH Method")
    canv = tk.Canvas(root, width=1000, height=600)
    canv.pack()
    # fig = plt.figure(dpi=90)
    fig = Figure(dpi=88)                        # using Figure to enable rotation
    plot = FigureCanvasTkAgg(fig, master=root)
    plot.draw()
    ax = ax3d.Axes3D(fig)
    # ax = fig.add_subplot(111, projection='3d')
    title = ax.set_title('')

    texts = ['Nt', 'd1', 'd2', 'd3', 'd4', 'd5'
             , 'l1', 'l2', 'l3', 'l4', 'l5'
             , 'alpha1', 'alpha2', 'alpha3', 'alpha4', 'alpha5']
    texts_theta = ['theta1 now', 'theta1 next', 'theta2 now', 'theta2 next'
                   , 'theta3 now', 'theta3 next', 'theta4 now', 'theta4 next', 'theta5 now', 'theta5 next']
    # fig parameters
    labels = [tk.Label(root) for i in range(len(texts))]
    [canv.create_window(120, 30 + i * 27, window=labels[i], anchor="e") for i in range(len(labels))]
    # fig angles
    labels_theta = [tk.Label(root) for i in range(len(texts_theta))]
    [canv.create_window(375, 30 + i * 27, window=labels_theta[i], anchor="e") for i in range(len(labels_theta))]

    params = [N, d_1, d_2, d_3, d_4, d_5, l_1, l_2, l_3, l_4, l_5, alpha_1, alpha_2, alpha_3, alpha_4, alpha_5]
    params_theta = [theta1_0, theta1_1, theta2_0, theta2_1
                    , theta3_0, theta3_1, theta4_0, theta4_1, theta5_0, theta5_1]

    # refresh
    def refresh_labels():
        for i in range(len(params)):
            labels[i]['text'] = texts[i] + ' = ' + str("{:.2f}".format(params[i]))
        for j in range(len(params_theta)):
            labels_theta[j]['text'] = texts_theta[j] + ' = ' + str("{:.2f}".format(params_theta[j]))

    refresh_labels()
    text_entry = [tk.Entry(root, width=10) for i in range(len(texts))]
    [canv.create_window(180, 30 + i * 27, window=tx) for i, tx in enumerate(text_entry)]
    text_entry_theta = [tk.Entry(root, width=10) for i in range(len(texts_theta))]
    [canv.create_window(430, 30 + i * 27, window=tx) for i, tx in enumerate(text_entry_theta)]

    def set_parameters():
        # for i in range(len(texts)):
        #    if text_entry[i].get():
        #        params[i] = float(text_entry[i].get())
        i, j = 0, 0
        while i < len(texts):
            if text_entry[i].get():
                params[i] = float(text_entry[i].get())
            i += 1
        # for j in range(len(texts_theta)):
        #    if text_entry_theta[j].get():
        #        params_theta[j] = float(text_entry_theta[j].get())
        while j < len(texts_theta):
            if text_entry_theta[j].get():
                params_theta[j] = float(text_entry_theta[j].get())
            j += 1
        refresh_labels()

    def set_theta_init():
        params_theta[::2] = params_theta[1::2]
        refresh_labels()

    def reset_button():
        for i in range(11, len(params)):
            params[i] = 0.0
        for j in range(0, len(params_theta)):
            params_theta[j] = 0.0
        clear_entry()
        refresh_labels()

    # init angles
    def set_pattern_one():
        params[11] = 90
        params[12:] = [0, 0, 0, 0]
        # '''
        for i in range(len(texts_theta)):
            if text_entry_theta[i].get():
                params_theta[:] = [90, 90, 45, 45, 45, 45, 45, 45, 45, 45]
            else:
                params_theta[1::2] = [90, 45, 45, 45, 45]
        # '''
        # params_theta[:] = [90, 90, 45, 45, 45, 45, 45, 45, 45, 45]
        # params_theta[1::2] = [90, 45, 45, 45, 45]
        refresh_labels()
        show_fig()

    # mode 2
    def set_pattern_two():
        params[11] = 90
        params[12:] = [0, 0, 0, 0]
        clear_entry()
        text_entry_theta[1].insert(tk.END, 180.0)
        text_entry_theta[3].insert(tk.END, 90.0)
        text_entry_theta[5].insert(tk.END, 60.0)
        text_entry_theta[7].insert(tk.END, 60.0)
        text_entry_theta[9].insert(tk.END, -30.0)
        refresh_labels()
        show_fig()

    # clear entry
    def clear_entry():
        for i in range(len(texts_theta)):
            if text_entry_theta[i].get():
                text_entry_theta[i].delete(0, tk.END)

    def show_fig():
        global ani_is_finished
        set_parameters()
        DH_calculation_list(params_theta, params[1:6], params[6:11], np.deg2rad(params[11:16]))
        ani_is_finished = False
        ani.event_source.start()
        # set_theta_init()

    DH_calculation_list(params_theta, params[1:6], params[6:11], np.deg2rad(params[11:16]))

    # plot size
    anim, = ax.plot([], [], [], 'o-k')
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.auto_scale_xyz([-3.5, 3.5], [-3.5, 3.5], [0, 5])
    # ax.auto_scale_xyz([-2, 2], [-2, 2], [0, 2])

    # animate update
    def ani_update(num, x0, y0, z0, line):
        global ani_is_finished
        # title.set_text('DH Method flame= {:d}'.format(num))
        x = anime_array[:N, 0, :6]
        y = anime_array[:N, 1, :6]
        z = anime_array[:N, 2, :6]
        if not ani_is_finished:
            new_x = x[num, :]
            new_y = y[num, :]
            new_z = z[num, :]
            line.set_data(new_x, new_y)
            line.set_3d_properties(new_z)
            if num >= (N - 1):
                ani_is_finished = True
                set_theta_init()
                ani.event_source.stop()
                # ani.event_source.interval = N
        else:
            new_x = x[N - 1, :]
            new_y = y[N - 1, :]
            new_z = z[N - 1, :]
            line.set_data(new_x, new_y)
            line.set_3d_properties(new_z)
        return line, title

    # interval - ms per frame
    # return FuncAnimation to ani
    ani = animation.FuncAnimation(fig, ani_update, fargs=(x, y, z, anim), frames=60, interval=10, blit=True)
    # plt.show()

    # btns
    btn_refresh = tk.Button(text='Set parameters', command=set_parameters)
    btn_reset = tk.Button(text='Reset parameters', command=reset_button)
    btn_run = tk.Button(text='Run', command=show_fig)
    btn_set_pattern = tk.Button(text='Set pattern 1', command=set_pattern_one)
    btn_clear_entry = tk.Button(text='Clear entry', command=clear_entry)
    btn_set_pattern_two = tk.Button(text='Set pattern 2', command=set_pattern_two)
    canv.create_window(430, 350, window=btn_refresh)
    canv.create_window(430, 400, window=btn_reset)
    canv.create_window(430, 450, window=btn_run)
    canv.create_window(300, 400, window=btn_set_pattern)
    canv.create_window(300, 350, window=btn_clear_entry)
    canv.create_window(300, 450, window=btn_set_pattern_two)
    toolbar = NavigationToolbar2Tk(plot, root)
    toolbar.update()
    canv.create_window(750, 300, window=plot.get_tk_widget())
    canv.create_window(450, 550, window=toolbar, anchor="w")
    root.mainloop()


if __name__ == '__main__':
    main()
